#!/usr/bin/env python

import rospy
from std_msgs.msg import String, Bool, Float64


lcd_pub = rospy.Publisher('lcd_display/line2', String, queue_size=10)
lcd_msg = String()
lcd.msg.data = "It's ALIVE!!!"

if __name__ == '__main__':
    rospy.init_node('lcd_demo_pub')
    while not rospy.is_shutdown():
        lcd_pub.publish(lcd_msg)
        rospy.sleep(15)