#!/usr/bin/env python

import rospy
import RPi.GPIO as GPIO
from std_msgs.msg import String

LED_PINS = (25, 5, 12)

led_array_modes = {'booting': (0, 0, 100, 'solid'), 'standby': (50, 50, 50, 'breathe'),
                   'alert': (100, 50, 25, 'rapid'), 'battery_low': (255, 255, 255, 'low_battery')}
effects = {'solid': 1, 'breathe': 0.5, 'rapid': 0.05, 'low_battery': 0.2}


class LedArray:
    def __init__(self, led_pins=LED_PINS):
        self.led_pins = led_pins
        self.pwm_r = None
        self.pwm_g = None
        self.pwm_b = None
        self.r = 0
        self.g = 0
        self.b = 0
        self.effect = 'solid'
        self.led_sub = rospy.Subscriber("/mode", String, self.cb_update_led, queue_size=10)

    def cb_update_led(self, msg):
        self.r = led_array_modes[msg.data[0]]
        self.g = led_array_modes[msg.data[1]]
        self.b = led_array_modes[msg.data[2]]
        self.effect = effects[led_array_modes[msg.data[3]]]

    def shine(self):
        if effect == 'solid' or effect == 'busy':
            self.pwm_r.ChangeDutyCycle(self.r)
            self.pwm_g.ChangeDutyCycle(self.g)
            self.pwm_b.ChangeDutyCycle(self.b)
        elif effect == 'low battery':
            self.pwm_r.ChangeDutyCycle(self.r)
            self.pwm_g.ChangeDutyCycle(self.g)
            self.pwm_b.ChangeDutyCycle(self.b)
            rospy.sleep(effects[effect]) #blink .._ (short short long)
            self.pwm_r.ChangeDutyCycle(self.r)
            self.pwm_g.ChangeDutyCycle(self.g)
            self.pwm_b.ChangeDutyCycle(self.b)
            rospy.sleep(effects[effect] * 5)
        else:
            for i in range(0, 101, 5):
                # Loop with dc set from 0 to 100 stepping dc up by 5 each loop
                self.pwm_r.ChangeDutyCycle(self.r * (i / 100))
                self.pwm_g.ChangeDutyCycle(self.g * (i / 100))
                self.pwm_b.ChangeDutyCycle(self.b * (i / 100))
                rospy.sleep(effects[effect])
            for i in range(95, 0, -5):
                self.pwm_r.ChangeDutyCycle(self.r * (i / 100))
                self.pwm_g.ChangeDutyCycle(self.g * (i / 100))
                self.pwm_b.ChangeDutyCycle(self.b * (i / 100))
                rospy.sleep(effects[effect])

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.led_pins, GPIO.OUT)
        self.pwm_r = GPIO.PWM(self.led_pins[0], 100)
        self.pwm_g = GPIO.PWM(self.led_pins[1], 100)
        self.pwm_b = GPIO.PWM(self.led_pins[2], 100)
        self.pwm_r.start(self.R)
        self.pwm_g.start(self.G)
        self.pwm_b.start(self.B)


if __name__ == '__main__':
    rospy.init_node('lcd_array')
    led = LedArray()
    led.setup()

    while not rospy.is_shutdown:
        led.shine()
