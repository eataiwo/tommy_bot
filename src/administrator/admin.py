#!/usr/bin/env python

import rospy
from std_msgs.msg import String
mode_publisher = rospy.Publisher('/mode', String , queue_size=10)

mode_msg = String()
mode = ['booting', 'standby', 'alert', 'low_battery', 'busy']
mode_select = 2 # placeholder variable

if __name__ == '__main__':
    rospy.init_node('administrator')
    mode_msg.data = mode[0]
    mode_publisher.publish(mode_msg)
    rospy.sleep(10)

    # For testing modes
    for i in mode:
        mode_msg.data = mode[i]
        mode_publisher.publish(mode_msg)
        rospy.sleep(5)

        rate = rospy.Rate(1)

    while not rospy.is_shutdown:
        mode_select = random(1,3)
        rospy.sleep(5)
        if mode_select = 1: # placeholder logic
            mode_msg.data = 'booting'
        elif mode_select = 2: # placeholder logic
            mode_msg.data = 'standby'
        elif mode_select = 3: # placeholder logic
            mode_msg.data = 'alert'

        mode_publisher.publish(mode_msg)
        rate.sleep()







