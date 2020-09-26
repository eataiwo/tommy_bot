#!/usr/bin/env python
"""
==================================================
Author: TJ Taiwo

Projects Referenced:
RpiMotorLib (Gavin Lyons) - https://github.com/gavinlyonsrepo/RpiMotorLib
gatoBot (Jorge Rancé) - https://github.com/jorgerance/gatoBot

==================================================
Numbering/Naming convention for wheels on Dexter
[1 , 2] [FL , FR]
[3 , 4] [RL , RR]
"""

import sys
import RPi.GPIO as GPIO
from time import sleep
import rospy
from src.powertrain.utils import stepdelay_check, speed_check, dist_2_steps, percent_to_stepdelay, stepdelay_to_percent, deg_2_steps
from std_msgs.msg import Float64, String, Bool

# Stepper motors are wired so all motors rotate its wheel forward when set to clockwise. i.e. the motors
# on the left hand side are wired with the opposite direction pins to the motors on the right hand side.

# If I implement a one way connector on the stepper motors the above wiring implementation will no long be ideal
# If so I will need to change it to accommodate this.


wheel_directions = {'forward': (0, 0, 0, 0), 'backward': (1, 1, 1, 1),
              'left': (1, 0, 0, 1), 'right': (0, 1, 1, 0),
              'cw': (0, 1, 0, 1), 'ccw': (1, 0, 1, 0)}

# TODO: Add these as ROS parameters
direction_pins = (27, 23, 19, 20)
step_pins = (22, 24, 26, 21)
enable_pin = 6

class Powertrain:
    """
    A class to control and interact with Dexter's powertrain.

    Attributes
    --------------
    direction_pins: GPIO pins connected to the direction pin on the stepper motor driver
    step_pins: GPIO pins connected to the step pin on the stepper motor driver
    directions: Dictionary that maps global directions to the individual wheel direction pins
    drive: Variable that tracks if the powertain is active or not
    remote_direction: Last direction sent from the web application

    Methods
    -------
    go():
        Moves Dexter based on desired direction, speed and distance.
    go_steps():
        Moves Dexter based on desired direction, step delay and number of steps
    remote():
        Moves Dexter based on commands from a web application
    stop():
        Stops Dexter
    setup():
        Setup for the powertrain
    """

    def __init__(self):
        self.direction_pins = direction_pins
        self.step_pins = step_pins
        self.enable_pin = enable_pin
        self.drive = False
        self.direction = ''
        self.speed = 80
        self.stepdelay = ''
        self.obstacle = False
        self.pwr_save = True

        self.powertrain_speed_subscriber = rospy.Subscriber("/powertrain/speed", Float64, self.cb_set_speed,
                                                            queue_size=10)
        self.powertrain_direction_subscriber = rospy.Subscriber("/powertrain/direction", String,
                                                                self.cb_set_direction, queue_size=10)
        self.powertrain_drive_subscriber = rospy.Subscriber("/powertrain/drive", Bool, self.cb_drive,
                                                            queue_size=10)
        self.powertrain_obstacle_subscriber = rospy.Subscriber("/sensors/ranging_FC", Float64,
                                                               self.cb_detect_obstacle, queue_size=10)

    def cb_set_speed(self, msg):
        self.speed = msg.data

    def cb_set_direction(self, msg):
        self.direction = msg.data
        rospy.loginfo('New direction received')
        # if not self.drive:
            # self.remote_control()

    def cb_drive(self, msg):

        self.drive = msg.data
        rospy.loginfo(f' drive state is {self.drive}')

        # TODO: Delete if new script working
        # if not self.drive and msg.data:
        #     self.drive = True
        # elif not msg.data:
        #     self.drive = False
        #     GPIO.output(self.step_pins, False)
        #     GPIO.output(self.direction_pins, False)

    def cb_detect_obstacle(self, msg):
        if msg.data < 20:
            self.obstacle = True
            #rospy.loginfo('Obstacle detected')
        else:
            self.obstacle = False
            #rospy.loginfo(f'No obstacle range is {msg.data}')

    def go(self, direction, distance, speed=0, initdelay=.05, verbose=False):
        """
        Moves Dexter based on desired direction, speed and distance.

        :param direction: Desired direction of Dexter.
        :param distance: Distance to be travelled in meters or degrees depending on direction.
        :param speed: Value from 0-100 for wheel speed.
        :param initdelay: Initial delay before motors begin moving.
        :param verbose: Prints information related to motor movement
        :type direction: str
        :type distance: int, float
        :type speed: int, float
        :type initdelay: int, float
        :type verbose: bool
        """

        # Convert distance or degrees to steps depending direction
        if direction in ['forward', 'backward', 'left', 'right']:
            steps = dist_2_steps(distance)[0]
        elif direction in ['cw', 'ccw']:
            steps = deg_2_steps(distance)[0]

        self.go_steps(direction, steps, percent_to_stepdelay(speed), initdelay, verbose)

    def go_steps(self, direction='forward', steps=100, stepdelay=.05, initdelay=0, verbose=False):
        """
        Moves Dexter based on desired direction, stepdelay and number of steps.

        :param direction: Desired direction of Dexter.
        :param steps: Steps stepper motor should turn.
        :param stepdelay: Delay between each step in seconds.
        :param initdelay: Initial delay before motors begin moving.
        :param verbose: Prints information related to motor movement
        :type direction: str
        :type steps: int
        :type stepdelay: int, float
        :type initdelay: int, float
        :type verbose: bool
        """

        stepdelay = stepdelay_check(stepdelay)
        # self.speed = stepdelay_to_percent(stepdelay)  # Update speed attribute

        self.direction = direction  # Update direction attribute

        GPIO.output(self.direction_pins, wheel_directions[direction])

        sleep(initdelay)

        GPIO.output(self.enable_pin, False)

        try:
            for i in range(steps):
                GPIO.output(self.step_pins, True)
                sleep(stepdelay)
                GPIO.output(self.step_pins, False)
                sleep(stepdelay)
                if verbose:
                    print(f'Steps count {i}')
        except KeyboardInterrupt:
            print('User Keyboard Interrupt @ Powertrain.go_steps()')
        except Exception as motor_error:
            print(sys.exc_info()[0])
            print(motor_error)
            print("Powertrain.go_steps(): Unexpected error:")
        else:
            if verbose:
                print(f'Direction = {direction}')
                print(f'Number of steps = {steps}')
                print(f'Step Delay = {stepdelay}')
                print(f'Initial delay = {initdelay}')
        finally:
            # cleanup
            GPIO.output(self.step_pins, False)
            GPIO.output(self.direction_pins, False)


    def remote(self, verbose=False):
        """
        Moves Dexter based on desired direction from web application.

        :param verbose: Prints information related to motor movement
        :type verbose: bool
        """

        self.drive = True

        # Set speed conversion according to the type of motion.
        # Implemented for better user control when using webapp.
        if self.direction in ['cw', 'ccw']:
            remote_speed_type = 'angular'
        else:
            remote_speed_type = 'linear'

        # Purpose delay to give time of user to look up from webapp before command is issued.
        sleep(0.2)
        GPIO.output(self.enable_pin, False)

        # Drive in direction commanded from webapp indefinitely
        while self.drive:
            self.go_steps(self.direction, 1, percent_to_stepdelay(self.speed, remote_speed_type), 0, verbose)

    def stop(self):
        """
        Stops powertrain
        """
        self.drive = False

        # Cleanup GPIO
        GPIO.output(self.step_pins, False)
        GPIO.output(self.direction_pins, False)

        #Delay to ensure stepper motors have brought robot to a standstill before turning off motors for power saving
        sleep(0.2)
        # Power save
        GPIO.output(self.enable_pin, True)

    def setup(self):
        """
        Setup for powertrain
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.direction_pins, GPIO.OUT)
        GPIO.setup(self.step_pins, GPIO.OUT)
        GPIO.setup(self.enable_pin, GPIO.OUT)
        GPIO.output(self.enable_pin, True)


if __name__ == "__main__":
    rospy.init_node('powertrain')

    dexter = Powertrain()
    dexter.setup()

    while True:
        # TODO: Delete if new script working
        # if dexter.pwr_save:
        #     rospy.sleep(1)
        #     GPIO.output(dexter.enable_pin, True)
        # else:
        #     GPIO.output(dexter.enable_pin, False)

        # TODO: Delete if new script working
        # if dexter.obstacle and dexter.remote_direction == 'forward':
        #     break
        #rospy.loginfo('Testing looping')

        # TODO: Delete if new script working
        # while dexter.drive:
        #     rospy.loginfo(f'remote direction is {dexter.remote_direction}')
        #     dexter.go_steps(dexter.remote_direction, 1, percent_to_stepdelay(dexter.speed), 0)
        if dexter.drive:
            # Set speed conversion according to the type of motion.
            # Implemented for better user control when using webapp.
            if dexter.direction in ['cw', 'ccw']:
                remote_speed_type = 'angular'
            else:
                remote_speed_type = 'linear'

            # Purpose delay to give time of user to look up from webapp before command is issued.
            #sleep(0.2)
            GPIO.output(dexter.enable_pin, False)

            # Drive in direction commanded from webapp indefinitely
            while dexter.drive:
                dexter.go_steps(dexter.direction, 1, percent_to_stepdelay(dexter.speed, remote_speed_type), 0)
        elif not dexter.drive:
            GPIO.output(dexter.step_pins, False)
            GPIO.output(dexter.direction_pins, False)
            sleep(0.2)
            GPIO.output(dexter.enable_pin, True)
