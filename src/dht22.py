import machine
import dht as dht_module
import ujson
import oled

class DHTSensor:
    def __init__(self, pin_number):
        self.sensor = dht_module.DHT22(machine.Pin(pin_number))
        
    def read(self):
        try:
            self.sensor.measure()
            temp = self.sensor.temperature()
            hum = self.sensor.humidity()
            return temp, hum
        except OSError as e:
            oled.show_message("Failed to read", "from DHT sensor.", 2)
            return None, None

    def to_json(self, temp, hum):
        return ujson.dumps({
            "temp": temp,
            "humidity": hum
        })
