🌱 MyPlant — Smart Irrigation & Environmental Monitoring System

MyPlant is an IoT-based smart irrigation and environmental monitoring system designed to automate plant care through real-time sensor acquisition, remote monitoring, and intelligent irrigation management.

The project integrates embedded devices, MQTT communication, Node-RED dashboards, and environmental sensors to provide automated plant health monitoring and irrigation control.

Main features:
- Real-time environmental monitoring & dashboard visualization
- Soil moisture, temperature and humidity detection and acquisition 
- Brightness monitoring
- Automated irrigation management
- Historical statistics and sensor tracking
- MQTT-based communication
- Remote monitoring interface


Featured technologies:
1. Embedded & IoT:
- MicroPython
- ESP32
- MQTT Protocol
- Node-RED

2. Sensors: 
- FC-28 Soil Moisture Sensor
- DHT Sensor
- LDR Sensor
- HC-SR04 Ultrasonic Sensor

3. Software & Dashboard
- Node-RED Dashboard
- CSS
- JSON Data Exchange


System architecture:
The system is composed of multiple sensors connected to an ESP32 microcontroller programmed in MicroPython.

Sensor data is collected and transmitted using the MQTT protocol to a Node-RED server, where:

- data is processed
- automation logic is executed
- dashboards are updated in real time
- irrigation control is managed

The platform provides both monitoring and automation functionalities for plant care management.


Sensor management:
- Soil Moisture Monitoring: the FC-28 sensor is used to detect soil moisture levels and determine irrigation requirements.

- Temperature & Humidity: environmental temperature and humidity are monitored using a DHT sensor.

- Brightness Monitoring: ambient light levels are acquired using an LDR sensor.

- Water Level Detection: an HC-SR04 ultrasonic sensor is used to monitor water tank levels.


Dashboard features:
- real-time charts
- historical data tables
- environmental statistics
- moisture tracking
- temperature and humidity visualization
- brightness monitoring
- system management controls


Future improvements:
- cloud integration
- AI-based irrigation prediction
- weather API integration
- mobile push notifications
- data analytics and forecasting
- energy optimization