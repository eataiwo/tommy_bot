#!/usr/bin/env python

import rospy
from std_msgs.msg import String


lcd_pub1 = rospy.Publisher('lcd_display/line1', String, queue_size=10)
lcd_pub2 = rospy.Publisher('lcd_display/line2', String, queue_size=10)
lcd_pub3 = rospy.Publisher('lcd_display/line3', String, queue_size=10)
lcd_pub4 = rospy.Publisher('lcd_display/line4', String, queue_size=10)

lcd_msg1 = String()
lcd_msg2 = String()
lcd_msg3 = String()
lcd_msg4 = String()


if __name__ == '__main__':
    rospy.init_node('lcd_demo_pub')

    while not rospy.is_shutdown():
        lcd_msg1.data = "I'm ALIVE!!!!"
        lcd_msg2.data = 'Come closer'
        # lcd_msg3.data = 'I want to tell'
        # lcd_msg4.data = 'you a secret'

        lcd_pub1.publish(lcd_msg1)
        #rospy.sleep(0.1)
        lcd_pub2.publish(lcd_msg2)
        #rospy.sleep(0.1)
        # lcd_pub3.publish(lcd_msg3)
        # rospy.sleep(0.1)
        # lcd_pub4.publish(lcd_msg4)
        # rospy.sleep(0.1)

        rospy.sleep(2)

        lcd_msg1.data = lcd_msg2.data = lcd_msg3.data = lcd_msg4.data = 'BOO!!!!!'

        lcd_pub1.publish(lcd_msg1)
        lcd_pub2.publish(lcd_msg2)
        rospy.sleep(2)
        # lcd_pub3.publish(lcd_msg3)
        # lcd_pub4.publish(lcd_msg4)
