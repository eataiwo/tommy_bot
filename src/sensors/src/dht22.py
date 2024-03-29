#!/usr/bin/python

import Adafruit_DHT
import rospy
from std_msgs.msg import Header
from sensor_msgs.msg import Temperature, RelativeHumidity

SENSOR_PIN = 13
temp_msg = Temperature()
hum_msg = RelativeHumidity()
header = Header()

class Dht22:
    def __init__(self, pin=SENSOR_PIN):
        self._sensor = Adafruit_DHT.DHT22
        self._pin = pin
        self.temp_pub = rospy.Publisher('sensors/air_temperature', Temperature, queue_size=10)
        self.hum_pub = rospy.Publisher('sensors/humidity', RelativeHumidity, queue_size=10)

    def read(self):
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, self._pin)
        if humidity is None or temperature is None:
            raise ValueError("Can't read DHT")
        return humidity, temperature


if __name__ == "__main__":
    rospy.init_node('dht22')
    dht22 = Dht22()
    rospy.sleep(2)
    while not rospy.is_shutdown():
        hum_msg.relative_humidity , temp_msg.temperature = dht22.read()
        hum_msg.relative_humidity = hum_msg.relative_humidity/100
        header.stamp = rospy.Time.now()
        header.frame_id = 'tommy'
        hum_msg.header = temp_msg.header = header
        dht22.hum_pub.publish(hum_msg)
        dht22.temp_pub.publish(temp_msg)
        rospy.sleep(2)
