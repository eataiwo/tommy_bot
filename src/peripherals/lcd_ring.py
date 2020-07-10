#!/usr/bin/env python

import time
import board
import neopixel
import rospy
from std_msgs.msg import String

PIXEL_PIN = board.D12  # On a Raspberry pi, use this instead, not all pins are supported
NUM_PIXELS = 12  # The number of NeoPixels
ORDER = neopixel.GRB  # The order of the pixel colors - RGB or GRB.

led_modes = {'booting': {'colour': (100, 100, 100), 'type': 'rainbow_cycle', 'on': 1, 'off': 0},
             'standby': {'colour': (75, 0, 130), 'type': 'pulse', 'on': 0.015, 'off': 0},
             'alert': {'colour': (255, 69, 0), 'type': 'blink', 'on': 1, 'off': 1},
             'battery_low': {'colour': (255, 0, 0), 'type': 'blink', 'on': 0.3, 'off': 0.2},
             'busy': {'colour': (255, 165, 0), 'type': 'solid', 'on': 1, 'off': 0}}
'''
Types are solid, blink, pulse, rainbow 
'''


class LedArray:
    def __init__(self, num_pixels=NUM_PIXELS, pixel_pin=PIXEL_PIN, order=ORDER):
        self.rgb = (0, 0, 0)
        self.num_pixel = num_pixels
        self.pixel_pin = pixel_pin
        self.order = order
        self.brightness = 0.8
        self.type = None
        self.on = None
        self.off = None

        self.led_sub = rospy.Subscriber("/mode", String, self.cb_update_led, queue_size=10)
        self.pixels = neopixel.NeoPixel(
            pixel_pin, num_pixels, brightness=self.brightness, auto_write=False, pixel_order=ORDER
        )

    def cb_update_led(self, msg):
        self.rgb = led_modes[msg.data]['colour']
        self.type = led_modes[msg.data]['type']
        self.on = led_modes[msg.data]['on']
        self.off = led_modes[msg.data]['off']

    def shine(self):
        if self.type == 'solid':
            self.solid()

        elif self.type == 'blink':
            self.blink()

        elif self.type == 'pulse':
            self.pulse()

        else:
            self.rainbow_cycle(0.002)

    def solid(self):
        self.pixels.fill(self.rgb)
        self.pixels.show()

    def blink(self):
        self.pixels.fill(self.rgb)
        self.pixels.show()
        rospy.sleep(self.on)

        self.pixels.fill((0, 0, 0))
        self.pixels.show()
        rospy.sleep(self.off)

    def double_blink(self):
        # blink .._ (short short long)
        self.pixels.fill(self.rgb)
        self.pixels.show()
        rospy.sleep(self.on)

        self.pixels.fill((0, 0, 0))
        self.pixels.show()
        rospy.sleep(self.off)

        self.pixels.fill(self.rgb)
        self.pixels.show()
        rospy.sleep(self.on * 5)

    def pulse(self):
        self.pixels.fill(self.rgb)
        self.pixels.show()
        max_brightness = self.pixels.brightness
        for i in range(99, 5, -1):
            if self.type == 'pulse':
                self.pixels.brightness =  (i * max_brightness)/100
                self.pixels.show()
                rospy.sleep(self.on)
            else:
                return
        for i in range(5, 101, 1):
            if self.type == 'pulse':
                self.pixels.brightness = (i * max_brightness)/100
                self.pixels.show()
                rospy.sleep(self.on)
            else:
                return

    def wheel(self, pos):
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
        if pos < 0 or pos > 255:
            r = g = b = 0
        elif pos < 85:
            r = int(pos * 3)
            g = int(255 - pos * 3)
            b = 0
        elif pos < 170:
            pos -= 85
            r = int(255 - pos * 3)
            g = 0
            b = int(pos * 3)
        else:
            pos -= 170
            r = 0
            g = int(pos * 3)
            b = int(255 - pos * 3)
        return r, g, b

    def rainbow_cycle(self, wait):
        for j in range(255):
            for i in range(self.num_pixel):
                pixel_index = (i * 256 // self.num_pixel) + j
                self.pixels[i] = self.wheel(pixel_index & 255)
            self.pixels.show()
            time.sleep(wait)


if __name__ == '__main__':
    rospy.init_node('lcd_array')
    led = LedArray()

    while not rospy.is_shutdown():
        led.shine()
