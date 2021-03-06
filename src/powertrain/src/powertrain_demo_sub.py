#!/usr/bin/env python
"""

"""

import rospy
from src.powertrain.powertrain import Powertrain
from std_msgs.msg import String, Bool, Float64


direction_pins = (27, 23, 19, 20)
step_pins = (22, 24, 26, 21)


class PowertrainDemo:
    def __init__(self):
        self.speed = None
        self.direction = None
        self.distance = None
        self.drive = None
        self.speed_sub = rospy.Subscriber("/powertrain/speed", Float64, self.callback_speed, queue_size=10)
        self.direction_sub = rospy.Subscriber("/powertrain/direction", String, self.callback_direction, queue_size=10)
        self.distance_sub = rospy.Subscriber("/powertrain/distance", Float64, self.callback_distance, queue_size=10)
        self.drive_sub = rospy.Subscriber("/powertrain/drive", Bool, self.callback_drive, queue_size=10)

    def callback_speed(self, msg):
        self.speed = msg.data

    def callback_direction(self, msg):
        self.direction = msg.data

    def callback_distance(self, msg):
        self.distance = msg.data

    def callback_drive(self, msg):
        self.drive = msg.data

    def start(self):
        #for i in range(5):
        while True:
            dexter.go_steps('forward', 1, 0.007, 0, False)


if __name__ == '__main__':
    dexter = Powertrain(direction_pins, step_pins)
    dexter.setup()
    rospy.init_node('powertrain_demo_sub')
    demo = PowertrainDemo()
    rospy.sleep(5.)
    demo.start()

