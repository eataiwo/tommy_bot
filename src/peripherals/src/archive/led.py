#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
LED_PINS = (25, 5, 12)

GPIO.setup(LED_PINS, GPIO.OUT)

pwm_r = GPIO.PWM(25, 1000)   # Initialize PWM on pwmPin 100Hz frequency
pwm_g = GPIO.PWM(5, 1000)
pwm_b = GPIO.PWM(12, 1000)
# main loop of program
print("\nPress Ctl C to quit \n")
dc = 0
# set dc variable to 0 (will start PWM at 0% duty cycle)
pwm_r.start(dc)
pwm_g.start(dc)
pwm_b.start(dc)
# Start PWM with 0% duty cycle
while True:
    # Create an infinite loop until Ctl C is pressed to stop program.
    for dc in range(0, 101, 5):
        # Loop with dc set from 0 to 100 stepping dc up by 5 each loop
        pwm_r.ChangeDutyCycle(dc)
        pwm_g.ChangeDutyCycle(dc)
        pwm_b.ChangeDutyCycle(dc)
        time.sleep(0.5)
# wait for .05 seconds at current LED brightness level
        print(dc)
    for dc in range(95, 0, -5):
        # Loop with dc set from 95 to 5 stepping dc down by 5 each loop
        pwm_r.ChangeDutyCycle(dc)
        pwm_g.ChangeDutyCycle(dc)
        pwm_b.ChangeDutyCycle(dc)
        time.sleep(0.5)
# wait for .05 seconds at current LED brightness level
        print(dc)

pwm_r.stop()
pwm_g.stop()
pwm_b.stop()

GPIO.cleanup()
