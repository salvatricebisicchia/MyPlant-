from machine import Pin, I2C, RTC 
from ssd1306 import SSD1306_I2C  
from time import sleep 
import network  
import ntptime  
import utime 
 
i2c = I2C(scl=Pin(22), sda=Pin(21))
oled = SSD1306_I2C(128, 64, i2c)

def clear():
    oled.fill(0)
    oled.show()

def show_message(line1, line2, duration):
    clear()
    oled.text(line1, 0, 10)
    oled.text(line2, 0, 20)
    oled.show()
    sleep(duration)
    clear()

def show_datetime():
    clear()
    
    rtc = RTC()  
    dt = list(rtc.datetime())  
    
    utc_offset = 2  
    dt[4] = (dt[4] + utc_offset) % 24
    
    if dt[4] < rtc.datetime()[4]:
        dt[2] += 1
    
    date_str = "{:04d}-{:02d}-{:02d}".format(dt[0], dt[1], dt[2])
    time_str = "{:02d}:{:02d}:{:02d}".format(dt[4], dt[5], dt[6])
    
    oled.text(date_str, 0, 10) 
    oled.text(time_str, 0, 20)  
    oled.show()  

