from dht22 import DHTSensor
from ldr import LDR
from fc28 import FC28
import hcsr04
import machine
import pump
import ujson
from umqtt.simple import MQTTClient
import ubinascii
import oled
from buzzer import BUZZER
import time

# Configurazione MQTT
mqtt_server = 'test.mosquitto.org'
client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = b'gruppo20'
topic_pub = b'myplant'
mqtt_user = ''
mqtt_pass = ''

# Definizione dei sensori
fc28 = FC28(machine.Pin(32))
dht = DHTSensor(machine.Pin(14))
ldr = LDR(34)
hcsr04 = hcsr04.HCSR04(trigger_pin=5, echo_pin=18, echo_timeout_us=10000)
b = BUZZER(23)
led = machine.Pin(27, machine.Pin.OUT)
led.off()
reset_button = machine.Pin(35, machine.Pin.IN, machine.Pin.PULL_DOWN)

# Definizione dei topic
topic_moisture = b'IoT_gruppo20/fc28'
topic_dht = b'IoT_gruppo20/dht'
topic_ldr = b'IoT_gruppo20/ldr'
topic_pump = b'IoT_gruppo20/pump' 
topic_reboot = b'IoT_gruppo20/reboot'
topic_hcsr04 = b'IoT_gruppo20/hcsr04'
topic_moisture_threshold = b'IoT_gruppo20/moisture_threshold'
topic_brightness_threshold = b'IoT_gruppo20/brightness_threshold'

# Definizione delle variabili globali
prev_weather = ''
prev_moisture = ''
prev_lightness = ''
prev_water_level = ''
distance_empty = 11.80  
distance_full = 4.19   
button_pressed = False
DEFAULT_MOISTURE_THRESHOLD = 50
MOISTURE_THRESHOLD = DEFAULT_MOISTURE_THRESHOLD
DEFAULT_BRIGHTNESS_THRESHOLD = 10
BRIGHTNESS_THRESHOLD = DEFAULT_BRIGHTNESS_THRESHOLD
manual_override = False

def sub_cb(topic, msg):
    global MOISTURE_THRESHOLD
    global BRIGHTNESS_THRESHOLD
    print((topic, msg))
    if topic == topic_pump:
        decoded_msg = msg.decode()
        if decoded_msg == 'pump':
            pump.activate_pump()
    elif topic == topic_reboot:
        decoded_msg = msg.decode()
        if decoded_msg == 'reboot':
            oled.show_message("Reboot command", "received.", 2)
            oled.show_message("Restarting...", "", 2)
            machine.reset()
    elif topic == topic_moisture_threshold:
        try:
            MOISTURE_THRESHOLD = float(msg.decode())
            #print("Moisture threshold updated to:", MOISTURE_THRESHOLD)  # Stampa di debug
            oled.show_message("Moisture treshold", str(MOISTURE_THRESHOLD), 2)
        except ValueError:
            print("Error during float conversion.")
    elif topic == topic_brightness_threshold:
        try:
            BRIGHTNESS_THRESHOLD = float(msg.decode())
            #print("Moisture threshold updated to:", BRIGHTNESS_THRESHOLD)  # Stampa di debug
            oled.show_message("Brightness treshold", str(BRIGHTNESS_THRESHOLD), 2)
        except ValueError:
            print("Error during float conversion.")

def connect_and_subscribe():
    global client_id, mqtt_server, topic_sub
    client = MQTTClient(client_id, mqtt_server, user=mqtt_user, password=mqtt_pass)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(topic_pump)
    client.subscribe(topic_reboot)
    client.subscribe(topic_hcsr04)
    client.subscribe(topic_moisture_threshold)
    client.subscribe(topic_brightness_threshold)
    print('Connected to %s MQTT broker, subscribed to %s and %s topics' % (mqtt_server, topic_sub, topic_pump))
    oled.show_message("Connected to", "MQTT broker.", 2)
    return client

def restart_and_reconnect():
    oled.show_message("Failed to connect", "to MQTT broker.", 2)
    oled.show_message("Reconnecting...", "", 2)
    time.sleep(10)
    machine.reset()

def check_ldr():
    print("Measuring light intensity... ", end="")
    ldr_value = ldr.value()
    if ldr_value < BRIGHTNESS_THRESHOLD:
        led.on()
    else:
        led.off()
    if ldr_value is not None:
        message = ldr.to_json(ldr_value)
        if message != prev_lightness:
            print("Updated!")
            print("Reporting to MQTT topic {}: {}".format(topic_ldr, message))
            client.publish(topic_ldr, message)
            return message
    print("No change")
    return prev_lightness

def check_dht():
    print("Measuring weather conditions... ", end="")
    temp, hum = dht.read()
    if temp is not None and hum is not None:
        message = dht.to_json(temp, hum)
        if message != prev_weather:
            print("Updated!")
            print("Reporting to MQTT topic {}: {}".format(topic_dht, message))
            client.publish(topic_dht, message)
            return message
    print("No change")
    return prev_weather

def check_fc28():
    global prev_moisture
    print("Measuring soil moisture... ", end="")
    moisture_percentage = fc28.value()
    if moisture_percentage is not None:
        message = fc28.to_json(moisture_percentage)
        if message != prev_moisture:
            print("Updated!")
            print("Reporting to MQTT topic {}: {}".format(topic_moisture, message))
            client.publish(topic_moisture, message)
            prev_moisture = message
            water_level_percentage = hcsr04.get_water_level_percentage(distance_empty, distance_full)
            # Controllo del livello di umidità e attivazione della pompa
            check_and_activate_pump(moisture_percentage, water_level_percentage)
            
            return message
    print("No change")
    return prev_moisture

def check_hcsr04():
    global prev_water_level  # Aggiungere global per poter modificare la variabile globale
    print("Measuring water level... ", end="")
    water_level_percentage = hcsr04.get_water_level_percentage(distance_empty, distance_full)
    if water_level_percentage is not None:
        message = ujson.dumps({"water_level_percentage": water_level_percentage})
        print("Reporting to MQTT topic {}: {}".format(topic_hcsr04, message))
        client.publish(topic_hcsr04, message)
        if water_level_percentage < 60:
            b.sound_alarm(3)
        prev_water_level = water_level_percentage
        return prev_water_level
    else:
        oled.show_message("Failed to measure", "water level.", 2)
        return prev_water_level
    
def check_button(pin):
    global button_pressed
    if pin.value() == 1:  # Se il pulsante è premuto e non è già stato rilevato
        button_pressed = True
        oled.show_message("Button pressed.", "Restarting...", 2)
        machine.reset()  
    elif pin.value() == 0:
        button_pressed = False  # Resetta lo stato del pulsante quando viene rilasciato

reset_button.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, handler=check_button)

def check_and_activate_pump(moisture_percentage, water_level_percentage):
    if not manual_override:
        if moisture_percentage < MOISTURE_THRESHOLD and moisture_percentage > 1:
            oled.show_message("Moisture below", "threshold!", 2)
            pump.activate_pump()
        elif moisture_percentage >= MOISTURE_THRESHOLD:
            print("Moisture above threshold, pump not activated.")
        else:
            print("Moisture non detected correctly, pump not activated.")
    else:
        print("Manual override is active, skipping automatic activation.")


try:
    client = connect_and_subscribe()
except OSError as e:
    restart_and_reconnect()
    
while True:
    try:
        client.check_msg()
        oled.show_datetime()
        prev_weather = check_dht()
        prev_water_level = check_hcsr04()
        prev_moisture = check_fc28()
        prev_lightness = check_ldr()
        time.sleep(3)
    except OSError as e:
        restart_and_reconnect()

