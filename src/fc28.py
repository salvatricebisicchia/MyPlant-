from machine import Pin, ADC
import ujson

class FC28:
    """This class reads a value from an FC-28 soil moisture sensor"""

    def __init__(self, pin, min_value=0, max_value=4095):
        """
        Initializes a new instance.
        :param pin: A pin that's connected to the FC-28 sensor.
        :param min_value: A minimum value that can be returned by the value() method.
        :param max_value: A maximum value that can be returned by the value() method.
        """
        if min_value >= max_value:
            raise ValueError('Min value must be less than max value')

        # Initialize ADC (analog to digital conversion)
        self.adc = ADC(Pin(pin))
        self.adc.atten(ADC.ATTN_11DB)
        self.adc.width(ADC.WIDTH_12BIT)
        self.min_value = min_value
        self.max_value = max_value

    def read(self):
        """
        Read a raw value from the FC-28 sensor.
        :return: A value from 0 to 4095.
        """
        return self.adc.read()

    def value(self):
        """
        Read a value from the FC-28 sensor in the specified range.
        :return: A value in percentage [0, 100] representing soil moisture.
        """
        raw_value = self.read()
        moisture_percentage = (self.max_value - raw_value) * 100 / (self.max_value - self.min_value)
        return round(moisture_percentage, 1)
    
    def to_json(self, moisture_percentage):
        """
        Convert the soil moisture value to JSON format.
        :param moisture_percentage: The moisture percentage value.
        :return: JSON formatted string.
        """
        return ujson.dumps({
            "moisture": moisture_percentage
        })
