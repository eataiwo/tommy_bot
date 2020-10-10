#!/usr/bin/env python

import rospy
import random
from std_msgs.msg import String

# Setup
mode_msg = String()
speech_msg = String()

mode = ['booting', 'standby', 'alert', 'low_battery', 'busy', 'shutting down', 'rebooting']


def cb_change_mode(msg):
    if msg.data in mode:
        mode_msg.data = msg.data
        mode_pub.publish(mode_msg)
        speech_msg.data = f'{msg.data} mode'
        speech_pub.publish(speech_msg)


if __name__ == '__main__':
    rospy.init_node('administrator')

    # Setup publisher and subscriber # Down the line a service maybe be more suited
    mode_pub = rospy.Publisher('/mode', String, queue_size=10)
    speech_pub = rospy.Publisher('/voice/speak', String, queue_size=10)
    mode_request_sub = rospy.Subscriber('/mode/request', String, cb_change_mode, queue_size=5)

    rospy.sleep(5)

    # Publish initial mode
    mode_msg.data = 'standby'
    mode_pub.publish(mode_msg)
    speech_msg.data = f'{mode_msg.data} mode'
    speech_pub.publish(speech_msg)

    rospy.spin()
