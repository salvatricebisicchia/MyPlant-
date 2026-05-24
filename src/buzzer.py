from machine import Pin, PWM
from time import sleep
import oled

class BUZZER:
    def __init__(self, sig_pin):
        self.pwm = PWM(Pin(sig_pin, Pin.OUT))
        self.pwm.duty(0)  

    def sound_alarm(self, duration):
        self.pwm.duty(512) 
        oled.show_message("Water level", "is too low!", 2)
        oled.show_message("Please refill.", "", 2)
        sleep(duration) 
        self.pwm.duty(0)  
