import network
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import micropython
import oled
import ntptime
import esp
esp.osdebug(None)
import gc
gc.collect()

# Configurazione Wi-Fi
ssid = 'iPhone di sasi'
password = 'sasina13'

def connect_wifi(ssid, password):
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        oled.show_message("Connecting to", "network...", 2)
        sta_if.active(True)
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            pass
    print('Network config:', sta_if.ifconfig())
    oled.show_message("Connected to", "network!", 2)


connect_wifi(ssid, password)
ntptime.settime()

import main
