#!/usr/bin/env python

"""
==================================================
Project: tommy_bot
Author: TJ Taiwo
Description: Script to define the powertrain class that handles the high-level control of the powertrain for tommy_bot
this class is able to take commands from the 'webapp node' or 'navigation node' to control where tommy_bot goes.

Projects referenced/used:
RpiMotorLib (Gavin Lyons) - https://github.com/gavinlyonsrepo/RpiMotorLib
gatoBot (Jorge Rancé) - https://github.com/jorgerance/gatoBot

==================================================
Notes:
Numbering/Naming convention for wheels on Dexter
[1 , 2] [FL , FR]
[3 , 4] [RL , RR]

Stepper motors are wired so all motors rotate its wheel forward when set to clockwise. i.e. the motors
on the left hand side are wired with the opposite direction pins to the motors on the right hand side.

If I implement a one way connector on the stepper motors the above wiring implementation will no long be valid.
If so I will need to change the wheel direction dictionary to accommodate this.

==================================================
"""

import sys
import RPi.GPIO as GPIO
import numpy as np
from time import sleep
import rospy
from utils import stepdelay_check, speed_check, dist_2_steps, percent_to_stepdelay, stepdelay_to_percent, deg_2_steps, steps_2_dist, steps_2_deg
from std_msgs.msg import Float64, String, Bool, Header 
from geometry_msgs.msg import Vector3, Twist, TwistWithCovariance, Pose, PoseWithCovariance, TransformStamped, Quaternion
from sensor_msgs.msg import Imu
from nav_msgs.msg import Odometry
import tf_conversions
import tf2_ros

# value of direction pins for the stepper drivers for global direction of tommy_bot
wheel_directions = {'forward': (0, 0, 0, 0), 'backward': (1, 1, 1, 1),
              'left': (1, 0, 0, 1), 'right': (0, 1, 1, 0),
              'cw': (0, 1, 0, 1), 'ccw': (1, 0, 1, 0)}

# GPIO pins connected to the stepper drivers directions pins
direction_pins = (27, 23, 19, 20)

# GPIO pins connected to the stepper drivers step pins
step_pins = (22, 24, 26, 21)

# GPIO pin connected to the stepper drivers enable pins - all pins are connected to one GPIO pin
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
        self.minimum_pulse_width = 0.001 # Smaller delay than can actually be achieved ...probably
        self.drive = False
        self.direction = ''
        self.speed = 80
        self.stepdelay = ''
        self.obstacle = False
        self.pwr_save = True
        self.location = [0, 0, 0]  # meters 
        self.orientation = [0, 0, 0]  # deg (yaw, pitch, roll)
        self.orientation_q = [0, 0, 0, 0] # Quaternion()
        self.linear_acceleration = [0, 0, 0]
        self.last_linear_acceleration = [0, 0, 0]
        self.angular_velocity = [0, 0, 0]
        self.linear_velocity = [0, 0, 0]
        self.imu_timestamp = None
        self.last_imu_timestamp = None
        self.header = Header()
        self.odometry_msg = Odometry()
        self.odom_trans = TransformStamped()

        # TODO: Add custom message so we can combine speed and direction into one topic.
        # Setup subscribers
        self.powertrain_speed_subscriber = rospy.Subscriber("/powertrain/speed", Float64, self.cb_set_speed,
                                                            queue_size=2)
        self.powertrain_direction_subscriber = rospy.Subscriber("/powertrain/direction", String,
                                                                self.cb_set_direction, queue_size=2)
        self.powertrain_drive_subscriber = rospy.Subscriber("/powertrain/drive", Bool, self.cb_drive,
                                                            queue_size=5)
        self.imu_subscriber = rospy.Subscriber("/sensors/imu/data", Imu ,
                                                               self.cb_imu, queue_size=10)
        self.odom_pub = rospy.Publisher('powertrain/odometry', Odometry, queue_size=10)

        # Setup transform broadcaster
        self.br = tf2_ros.TransformBroadcaster()

    def cb_set_speed(self, msg):
        self.speed = msg.data

    def cb_set_direction(self, msg):
        self.direction = msg.data
        # rospy.loginfo('New direction received')  # For debugging

    def cb_drive(self, msg):

        self.drive = msg.data

    def cb_detect_obstacle(self, msg):
        if msg.data < 20:
            self.obstacle = True
            # rospy.loginfo('Obstacle detected')  # For debugging
        else:
            self.obstacle = False
            # rospy.loginfo(f'No obstacle2 range is {msg.data}')  # For debugging
    def cb_imu(self, msg):
        self.linear_acceleration = msg.linear_acceleration
        self.angular_velocity = msg.angular_velocity
        self.imu_timestamp = msg.header.stamp

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

        self.direction = direction  # Update direction attribute

        GPIO.output(self.direction_pins, wheel_directions[direction])

        sleep(initdelay)

        GPIO.output(self.enable_pin, False)

        try:
            for i in range(steps):
                GPIO.output(self.step_pins, True)
                sleep(self.minimum_pulse_width) # Minimum pulse width
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
    
    def get_pose(self, steps):    
        # So if I have rotated by an angle theta when going forward relative to the robot it is actually going an components forward and a componenet sideways relative to the orginal 
        # co-ordinate system. Therefore I have to take into account linear motion based on theta. Cases to consider theta = 0, 30, 45, 90, 180, 270, 360, 720.
        
        #Update on the above, I believe this is the whole point of the odom base_link tf module thing. 
            
        if self.direction == 'forward':
            distance = steps_2_dist(steps)
            self.location[0] += distance
        elif self. direction == 'backward':
            distance = steps_2_dist(steps)
            self.location[0] -= distance
        elif self.direction == 'left': 
            distance = steps_2_dist(steps)
            self.location[1] -= distance
        elif self.direction == 'right':
            distance = steps_2_dist(steps)
            self.location[1] += distance
        elif self.direction == 'cw':
            turn = steps_2_deg(steps)
            self.orientation[0] += turn  # I could get this from the imu/data topic but will need to test how accurate it is or do some sensor fusion. 
            self.orientation_q = tf_conversions.transformations.quaternion_from_euler(0 ,0 ,self.orientation[0])
        elif self.direction == 'ccw':
            turn = steps_2_deg(steps)
            self.orientation[0] -= turn 
            self.orientation_q = tf_conversions.transformations.quaternion_from_euler(0 ,0 ,self.orientation[0])
        else:
            pass  #  print error about not being able to update odometry
        
    def get_twist(self):
        
        if self.last_imu_timestamp != None:
            
            dt = (self.imu_timestamp - self.last_imu_timestamp).to_sec()
        
            self.linear_velocity[0] += dt*((self.last_linear_acceleration.x+self.linear_acceleration.x)/2)
            self.linear_velocity[1] += dt*((self.last_linear_acceleration.y+self.linear_acceleration.y)/2)
            self.linear_velocity[2] += dt*((self.last_linear_acceleration.z+self.linear_acceleration.z)/2)  # Do not need to delete/comment out eventually to save computational power
        
        self.last_imu_timestamp = self.imu_timestamp
        self.last_linear_acceleration = self.linear_acceleration 
        
        
    # def euler_to_quaternion(self, r): # Make hidden method with a underscore 
        # (yaw, pitch, roll) = np.deg2rad([r[0], r[1], r[2]])
        # qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
        # qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
        # qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
        # qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
        # return [qx, qy, qz, qw]
    
    def pub_odometry(self):
        # Lets start with header
        self.odometry_msg.header.stamp = self.imu_timestamp # Incase the imu values have been update this should have the timestamp from the data that will now be used. 
        self.odometry_msg.header.frame_id = 'odom'
        
        # Pose
        self.odometry_msg.pose.pose.position.x = self.location[0]
        self.odometry_msg.pose.pose.position.y = self.location[1]
        self.odometry_msg.pose.pose.position.z = 0
        
        self.odometry_msg.pose.pose.orientation.x = self.orientation_q[0]
        self.odometry_msg.pose.pose.orientation.y = self.orientation_q[1]
        self.odometry_msg.pose.pose.orientation.z = self.orientation_q[2]
        self.odometry_msg.pose.pose.orientation.w = self.orientation_q[3]
        
        # Twist
        self.odometry_msg.child_frame_id = 'base_link'
        self.odometry_msg.twist.twist.linear.x = self.linear_acceleration.x
        self.odometry_msg.twist.twist.linear.y = self.linear_acceleration.y
        self.odometry_msg.twist.twist.angular.z = self.angular_velocity.z 
        
        self.odom_pub.publish(self.odometry_msg)
        
        # Broadcast transformation
        self.odom_trans.header.stamp = self.imu_timestamp
        self.odom_trans.header.frame_id = 'odom'
        self.odom_trans.child_frame_id = 'base_link'
        self.odom_trans.transform.translation.x = self.location[0]
        self.odom_trans.transform.translation.y = self.location[1]
        self.odom_trans.transform.translation.z = 0.0
        self.odom_trans.transform.rotation.x = self.orientation_q[0]
        self.odom_trans.transform.rotation.y = self.orientation_q[1]
        self.odom_trans.transform.rotation.z = self.orientation_q[2]
        self.odom_trans.transform.rotation.w = self.orientation_q[3]
        
        self.br.sendTransform(self.odom_trans)
        

if __name__ == "__main__":
    rospy.init_node('powertrain')

    dexter = Powertrain()
    dexter.setup()
    step_size = 1
    


    while not rospy.is_shutdown():
        if dexter.drive:
            # Set speed conversion according to the type of motion.
            # Implemented for better user control when using webapp.
            if dexter.direction in ['cw', 'ccw']:
                remote_speed_type = 'angular'
            else:
                remote_speed_type = 'linear'

            GPIO.output(dexter.enable_pin, False)

            # Drive in direction commanded from webapp indefinitely
            while not rospy.is_shutdown and dexter.drive:
                dexter.go_steps(dexter.direction, step_size, percent_to_stepdelay(dexter.speed, remote_speed_type), 0)
                dexter.get_pose(step_size)
                dexter.get_twist()
                dexter.pub_odometry()
                
        elif not dexter.drive:
            GPIO.output(dexter.step_pins, False)
            GPIO.output(dexter.direction_pins, False)
            sleep(0.2)
            GPIO.output(dexter.enable_pin, True)
