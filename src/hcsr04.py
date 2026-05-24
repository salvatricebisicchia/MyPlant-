from machine import Pin, time_pulse_us, PWM
from utime import sleep_us, sleep

class HCSR04:
    distance_empty = 12.68  
    distance_full = 2.51   

    def __init__(self, trigger_pin, echo_pin, echo_timeout_us=500*2*30):
        self.echo_timeout_us = echo_timeout_us
        self.trigger = Pin(trigger_pin, mode=Pin.OUT, pull=None)
        self.trigger.value(0)
        self.echo = Pin(echo_pin, mode=Pin.IN, pull=None)

    def _send_pulse_and_wait(self):
        self.trigger.value(0)
        sleep_us(5)
        self.trigger.value(1)
        sleep_us(10)
        self.trigger.value(0)
        try:
            pulse_time = time_pulse_us(self.echo, 1, self.echo_timeout_us)
            if pulse_time < 0:
                MAX_RANGE_IN_CM = 7
                pulse_time = int(MAX_RANGE_IN_CM * 29.1)
            return pulse_time
        except OSError as ex:
            if ex.args[0] == 110:
                raise OSError('Out of range')
            raise ex

    def distance_cm(self):
        pulse_time = self._send_pulse_and_wait()
        cms = (pulse_time / 2) / 29.1
        return cms

    def get_water_level_percentage(self, distance_empty, distance_full):
        distance_cm = self.distance_cm()

        if distance_cm < distance_full:
            distance_cm = distance_full
        elif distance_cm > distance_empty:
            distance_cm = distance_empty

        # Calcolo del livello dell'acqua in cm
        water_height_cm = distance_empty - distance_cm

        # Calcolo del livello dell'acqua in percentuale
        max_water_height = distance_empty - distance_full
        water_level_percentage = (water_height_cm / max_water_height) * 100
        return water_level_percentage
