#!/usr/bin/python

# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# adapted for SensemakersAMS Astroplant Explorer
# make sure to install the Adafruit_DHT module first with 'sudo pip3 install Adafruit_DHT'

import Adafruit_DHT
import rospy
from time import sleep
from std_msgs.msg import Float64

SENSOR_PIN = 13
temp_msg = Float64()
hum_msg = Float64()


class Dht22:
    def __init__(self, pin=SENSOR_PIN):
        self._sensor = Adafruit_DHT.DHT22
        self._pin = pin
        self.temp_pub = rospy.Publisher('_sensors/air_temperature', Float64, queue_size=10)
        self.hum_pub = rospy.Publisher('_sensors/humidity', Float64, queue_size=10)

    def read(self):
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, self._pin)
        if humidity is None or temperature is None:
            raise ValueError("Can't read DHT")
        return humidity, temperature


if __name__ == "__main__":
    rospy.init_node('dht22')
    while not rospy.is_shutdown():
        dht22 = Dht22()
        hum_msg.data, temp_msg.data = dht22.read()
        dht22.hum_pub.publish(hum_msg)
        dht22.temp_pub.publish(temp_msg)
        rospy.sleep(5)