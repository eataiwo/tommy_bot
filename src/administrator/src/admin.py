#!/usr/bin/env python

import rospy
import random
from std_msgs.msg import String

# Setup
mode_msg = String()
mode = ['booting', 'standby', 'alert', 'low_battery', 'busy']


def cb_change_mode(msg):
    if msg.data in mode:
        mode_msg.data = msg.data
        mode_pub.publish(mode_msg)


if __name__ == '__main__':
    rospy.init_node('administrator')

    # Setup publisher and subscriber # Down the line a service maybe be more suited
    mode_pub = rospy.Publisher('/mode', String, queue_size=10)
    mode_request_sub = rospy.Subscriber('/mode/request', String, cb_change_mode, queue_size=5)

    rospy.spin()
