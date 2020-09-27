#!/usr/bin/env python

import rospy
import random
from std_msgs.msg import String

mode_req_msg = String()
mode = ['booting', 'standby', 'alert', 'low_battery', 'busy']
mode_select = 0

if __name__ == '__main__':
    rospy.init_node('mode_change_request_pub')
    mode_req = rospy.Publisher('/mode/request', String, queue_size=5)

    # For testing modes
    mode_req_msg.data = mode[0]
    mode_req.publish(mode_req_msg)
    rospy.sleep(5)

    for i in mode:
        mode_req_msg.data = i
        mode_req.publish(mode_req_msg)
        rospy.sleep(5)

        rate = rospy.Rate(1)

    while not rospy.is_shutdown():
        mode_select = random.randint(1, 5)
        rospy.sleep(10)
        if mode_select == 1:  # placeholder logic
            mode_req_msg.data = 'booting'
        elif mode_select == 2:  # placeholder logic
            mode_req_msg.data = 'standby'
        elif mode_select == 3:  # placeholder logic
            mode_req_msg.data = 'alert'
        elif mode_select == 4:
            mode_req_msg.data = 'battery_low'
        elif mode_select == 5:
            mode_req_msg.data = 'busy'

        mode_req.publish(mode_req_msg)

        rate.sleep()

