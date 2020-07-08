#!/usr/bin/env python

import RPi.GPIO as GPIO
import time

# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 16

# set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

range_msg = Float64()

class Hcsr04:
    def __init__(self, trigger=GPIO_TRIGGER, echo=GPIO_ECHO):
        self._trigger = trigger
        self._echo = echo
        self.air_temp = None
        self.hum = None
        # Ensure this is the ambient temperature not the air temperature inside Dexter
        self.temp_sub = rospy.Subscriber("sensors/temperature", Float64, self.cb_update_air_temp, queue_size=10)
        self.hum_sub = rospy.Subscriber("sensors/humidity", Float64, self.cb_update_hum, queue_size=10)
        self.range_pub = rospy.Publisher('sensors/ranging_FC', Float64, queue_size=10)

    def distance(self):
        # set Trigger to HIGH
        GPIO.output(GPIO_TRIGGER, True)

        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)

        StartTime = time.time()
        StopTime = time.time()

        # save StartTime
        while GPIO.input(GPIO_ECHO) == 0:
            StartTime = time.time()

        # save time of arrival
        while GPIO.input(GPIO_ECHO) == 1:
            StopTime = time.time()

        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        if self.air_temp is None or self.hum is None:
            rospy.sleep(10)
        c = 331.3 + (0.606 * self.air_temp) + (0.0124 * self.hum)  # speed of sound
        distance = (TimeElapsed * c * 100) / 2  # cm

        return distance

    def cb_update_air_temp(self, msg):
        self.air_temp = msg.data

    def cb_update_hum(self, msg):
        self.hum = msg.data


if __name__ == '__main__':
    rospy.init_node(ultrasonic)
    rospy.Rate(10)
    hcsr04 = Hcsr04()

    try:
        range_msg.data = hcsr04.distance()
    except Exception as error:
        print(error)
        GPIO.cleanup()

    hcsr04.range_pub.publish(range_msg)


