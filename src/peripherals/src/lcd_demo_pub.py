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

test_string = ["I'm ALIVE!!!!", 'Come closer', 'I want to tell', 'you a secret', 'BOO!!!!!']


if __name__ == '__main__':
    rospy.init_node('lcd_demo_pub')
    while not rospy.is_shutdown():
        lcd_msg1.data = test_string[0]
        lcd_msg2.data = test_string[1]
        lcd_msg3.data = test_string[2]
        lcd_msg4.data = test_string[3]

        lcd_pub1.publish(lcd_msg1)
        lcd_pub2.publish(lcd_msg2)
        lcd_pub3.publish(lcd_msg3)
        lcd_pub4.publish(lcd_msg4)

        rospy.sleep(20)

        lcd_msg1.data, lcd_msg2.data, lcd_msg3.data,lcd_msg4.data = test_string[4]

        lcd_pub1.publish(lcd_msg1)
        lcd_pub2.publish(lcd_msg2)
        lcd_pub3.publish(lcd_msg3)
        lcd_pub4.publish(lcd_msg4)
