#!/usr/bin/env python

import rospy
import RPi.GPIO as GPIO
from std_msgs.msg import String

LED_PINS = (25, 5, 12)

led_array_modes = {'booting': (100, 100, 100, 'solid'), 'standby': (100, 100, 100, 'breathe'),
                   'alert': (100, 100, 100, 'rapid'), 'battery_low': (100, 100, 100, 'low_battery'),
                   'busy':(100, 100, 0, 'solid')}
effects = {'solid': 1, 'breathe': 0.1, 'rapid': 0.5, 'low_battery': 0.1}


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
        self.r = led_array_modes[msg.data][0]
        self.g = led_array_modes[msg.data][1]
        self.b = led_array_modes[msg.data][2]
        self.effect = led_array_modes[msg.data][3]

    def shine(self):
        if self.effect == 'solid' or self.effect == 'busy':
            #rospy.loginfo(self.effect)
            
            self.pwm_r.ChangeDutyCycle(self.r)
            self.pwm_g.ChangeDutyCycle(self.g)
            self.pwm_b.ChangeDutyCycle(self.b)
            
        elif self.effect == 'low battery':
            #rospy.loginfo(self.effect)
            
            self.pwm_r.ChangeDutyCycle(self.r)
            self.pwm_g.ChangeDutyCycle(self.g)
            self.pwm_b.ChangeDutyCycle(self.b)
            rospy.sleep(effects[self.effect]) #blink .._ (short short long)
            
            self.pwm_r.ChangeDutyCycle(0)
            self.pwm_g.ChangeDutyCycle(0)
            self.pwm_b.ChangeDutyCycle(0)
            rospy.sleep(effects[self.effect])
            
            self.pwm_r.ChangeDutyCycle(self.r)
            self.pwm_g.ChangeDutyCycle(self.g)
            self.pwm_b.ChangeDutyCycle(self.b)
            rospy.sleep(effects[self.effect] * 5)
            
        elif self.effect == 'breathe':
            #rospy.loginfo(self.effect)
        
            d = rospy.Duration(effects[self.effect]) 
            for i in range(0, 101, 5):
                # Loop with dc set from 0 to 100 stepping dc up by 5 each loop
                self.pwm_r.ChangeDutyCycle(self.r * (i / 100))
                self.pwm_g.ChangeDutyCycle(self.g * (i / 100))
                self.pwm_b.ChangeDutyCycle(self.b * (i / 100))
                rospy.sleep(d)
            for i in range(95, 0, -5):
                self.pwm_r.ChangeDutyCycle(self.r * (i / 100))
                self.pwm_g.ChangeDutyCycle(self.g * (i / 100))
                self.pwm_b.ChangeDutyCycle(self.b * (i / 100))
                rospy.sleep(d)
        else: 
            #rospy.loginfo(self.effect)
        
            self.pwm_r.ChangeDutyCycle(self.r)
            self.pwm_g.ChangeDutyCycle(self.g)
            self.pwm_b.ChangeDutyCycle(self.b)
            rospy.sleep(effects[self.effect]) #blink .._ (short short long)
            
            self.pwm_r.ChangeDutyCycle(0)
            self.pwm_g.ChangeDutyCycle(0)
            self.pwm_b.ChangeDutyCycle(0)
            rospy.sleep(effects[self.effect])

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.led_pins, GPIO.OUT)
        self.pwm_r = GPIO.PWM(self.led_pins[0], 100)
        self.pwm_g = GPIO.PWM(self.led_pins[1], 100)
        self.pwm_b = GPIO.PWM(self.led_pins[2], 100)
        self.pwm_r.start(self.r)
        self.pwm_g.start(self.g)
        self.pwm_b.start(self.b)


if __name__ == '__main__':
    rospy.init_node('lcd_array')
    led = LedArray()
    led.setup()

    while not rospy.is_shutdown():
        led.shine()
    
