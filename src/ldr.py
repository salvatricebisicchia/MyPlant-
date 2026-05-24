from machine import ADC, Pin
import time
import ujson

class LDR:
    """This class read a value from a light dependent resistor (LDR)"""

    def __init__(self, pin, min_value=0, max_value=100):
        """
        Initializes a new instance.
        :parameter pin A pin that's connected to an LDR.
        :parameter min_value A min value that can be returned by value() method.
        :parameter max_value A max value that can be returned by value() method.
        """
        if min_value >= max_value:
            raise Exception('Min value is greater or equal to max value')

        self.adc = ADC(Pin(pin))
        self.min_value = min_value
        self.max_value = max_value

    def read(self):
        """
        Read a raw value from the LDR.
        :return a value from 0 to 4095.
        """
        return self.adc.read()

    def value(self):
        """
        Read a value from the LDR in the specified range.
        :return a value from the specified [min, max] range.
        """
        return (self.max_value - self.min_value) * self.read() / 4095

    def to_json(self, ldr_value):
        """
        Convert the LDR value to JSON format.
        :param ldr_value: The value read from the LDR.
        :return: A JSON string representing the LDR value.
        """
        return ujson.dumps({
            "brightness": ldr_value
        })
