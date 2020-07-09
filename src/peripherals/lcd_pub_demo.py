#!/usr/bin/env python

import rospy
from std_msgs.msg import String


lcd_pub = rospy.Publisher('lcd_display/line2', String, queue_size=10)
lcd_msg = String()
test_string = ["It's ALIVE!!!!", 'Come closer', 'I want to tell', 'you a secret']


if __name__ == '__main__':
    rospy.init_node('lcd_demo_pub')
    while not rospy.is_shutdown():
        for i in test_string:
            lcd_msg.data = i 
            lcd_pub.publish(lcd_msg)
            rospy.sleep(5.)
