from machine import Pin
import time
import oled

relay = Pin(26, Pin.OUT)
relay.value(1)

button = Pin(25, Pin.IN, Pin.PULL_DOWN)

MIN_INTERVAL = 600 

last_pump_activation = 0

manual_override = False

def activate_pump():
    global last_pump_activation
    current_time = time.time()
    if (current_time - last_pump_activation) > MIN_INTERVAL:
        oled.show_message("Activating", "pump.", 2)
        relay.value(0)
        time.sleep(3)
        relay.value(1)
        last_pump_activation = current_time
        oled.show_message("Pump", "deactivated.", 2)
    else:
        print("Pump activation skipped. Waiting for the minimum interval.")

def manual_control(pin):
    global manual_override
    if pin.value() == 1:  
        manual_override = not manual_override
        if manual_override:
            relay.value(0)
            oled.show_message("Pump ON.", "", 3)
        else:
            relay.value(1)
            oled.show_message("Pump OFF.", "", 2)

button.irq(trigger=Pin.IRQ_RISING, handler=manual_control)


