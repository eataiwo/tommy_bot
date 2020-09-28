#!/usr/bin/env python

"""
Control the 16x2 LCD display with Hitachi controller.
See https: // github.com/sensemakersamsterdam/astroplant_explorer
"""
# Reworked version from https://raspberrytips.nl/i2c-lcd-scherm/
# (c) portions by Sensemakersams.org and others.
# See https://github.com/sensemakersamsterdam/astroplant_explorer
# Author: Gijs Mos
#
#

import smbus
import rospy
from std_msgs.msg import String

# Define some device parameters
I2C_ADDR = 0x27  # I2C device address
LCD_WIDTH = 20  # Maximum characters per line

# Define some device constants
LCD_CHR = 1  # Mode - Sending data
LCD_CMD = 0  # Mode - Sending command

LCD_LINE_1 = 0x80  # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0  # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94  # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4  # LCD RAM address for the 4th line

LCD_BACKLIGHT = 0x08  # On
# LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100  # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

# Open I2C interface
# bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1)  # Rev 2 Pi uses 1


class Lcd:
    """Class to control the 16x2 LCD display with Hitachi controller.
    """

    def __init__(self, i2c_address=I2C_ADDR, i2c_bus=1):
        self._addr = i2c_address
        self._bus_number = i2c_bus
        self._bus = None
        self._n_err = 0
        self._backlight = None
        self.robot_mode = ''
        self.lcd_sub = rospy.Subscriber("/lcd_display/line1", String, self.cb_display_line1, queue_size=10)
        self.lcd_sub = rospy.Subscriber("/lcd_display/line2", String, self.cb_display_line2, queue_size=10)
        self.lcd_sub = rospy.Subscriber("/lcd_display/line3", String, self.cb_display_line3, queue_size=10)
        self.lcd_sub = rospy.Subscriber("/lcd_display/line4", String, self.cb_display_line4, queue_size=10)
        self.lcd_sub = rospy.Subscriber("/mode", String, self.cb_current_mode, queue_size=10)

    def setup(self):
        # Initialise display
        self.lcd_byte(0x33, LCD_CMD)  # 110011 Initialise
        self.lcd_byte(0x32, LCD_CMD)  # 110010 Initialise
        self.lcd_byte(0x06, LCD_CMD)  # 000110 Cursor move direction
        self.lcd_byte(0x0C, LCD_CMD)  # 001100 Display On,Cursor Off, Blink Off
        self.lcd_byte(0x28, LCD_CMD)  # 101000 Data length, number of lines, font size
        self.lcd_byte(0x01, LCD_CMD)  # 000001 Clear display
        rospy.sleep(E_DELAY)

    def lcd_toggle_enable(self, bits):
        # Toggle enable
        rospy.sleep(E_DELAY)
        bus.write_byte(self._addr, (bits | ENABLE))
        rospy.sleep(E_PULSE)
        bus.write_byte(self._addr, (bits & ~ENABLE))
        rospy.sleep(E_DELAY)

    def lcd_byte(self, bits, mode):
        # Send byte to data pins
        # bits = the data
        # mode = 1 for data
        #        0 for command

        bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
        bits_low = mode | ((bits << 4) & 0xF0) | LCD_BACKLIGHT

        # High bits
        bus.write_byte(self._addr, bits_high)
        self.lcd_toggle_enable(bits_high)

        # Low bits
        bus.write_byte(self._addr, bits_low)
        self.lcd_toggle_enable(bits_low)

    def lcd_string(self, message, line):
        # Send string to display

        message = message.ljust(LCD_WIDTH, " ")

        self.lcd_byte(line, LCD_CMD)

        for i in range(LCD_WIDTH):
            self.lcd_byte(ord(message[i]), LCD_CHR)

    def cb_display_line1(self, msg):
        self.lcd_string(msg.data, LCD_LINE_1)
        rospy.sleep(5.)
        self.lcd_string(f'Mode: {self.robot_mode}', LCD_LINE_1)

    def cb_display_line2(self, msg):
        self.lcd_string(msg.data, LCD_LINE_2)
        rospy.sleep(5.)

    def cb_display_line3(self, msg):
        self.lcd_string("Basic testing", LCD_LINE_3)
        rospy.sleep(5.)

    def cb_display_line4(self, msg):
        self.lcd_string(msg.data, LCD_LINE_4)
        rospy.sleep(5.)

    def cb_current_mode(self, msg):
        self.robot_mode = msg.data


if __name__ == '__main__':
    rospy.init_node('lcd_display')

    lcd = Lcd()
    lcd.setup()

    lcd.lcd_string('Starting up', LCD_LINE_1)
    rospy.sleep(2)

    lcd.lcd_string('Ready', LCD_LINE_1)
    rospy.sleep(3)

    lcd.lcd_string('Monday', LCD_LINE_1)
    lcd.lcd_string('Tuesday', LCD_LINE_2)
    lcd.lcd_string('Wednesday', LCD_LINE_3)
    lcd.lcd_string('Thursday', LCD_LINE_4)
    rospy.sleep(5)

    rospy.spin()
