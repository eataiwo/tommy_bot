#!/usr/bin/env python

import rospy
from std_msgs.msg import String

lcd_pub1 = rospy.Publisher('lcd_display/line1', String, queue_size=10)
lcd_pub2 = rospy.Publisher('lcd_display/line2', String, queue_size=10)
lcd_pub3 = rospy.Publisher('lcd_display/line3', String, queue_size=10)
lcd_pub4 = rospy.Publisher('lcd_display/line4', String, queue_size=10)
speak_pub = rospy.Publisher('voice/speak', String, queue_size=10)

lcd_msg1 = String()
lcd_msg2 = String()
lcd_msg3 = String()
lcd_msg4 = String()
speech_msg = String()

if __name__ == '__main__':
    rospy.init_node('lcd_demo_pub')

    lcd_msg1.data = "I'm ALIVE!!!!"
    lcd_pub1.publish(lcd_msg1)
    rospy.sleep(0.2)

    while not rospy.is_shutdown():
        lcd_msg2.data = 'Come closer'
        lcd_msg3.data = 'I want to tell'
        lcd_msg4.data = 'you a secret'

        lcd_pub2.publish(lcd_msg2)
        rospy.sleep(1)
        lcd_pub3.publish(lcd_msg3)
        rospy.sleep(1)
        lcd_pub4.publish(lcd_msg4)
        rospy.sleep(1)

        rospy.sleep(5)

        lcd_msg2.data = lcd_msg3.data = lcd_msg4.data = 'BOO'
        speech_msg.data = 'BO'
        rospy.loginfo(f'{lcd_msg2.data} {lcd_msg3.data} {lcd_msg4.data}')

        lcd_pub2.publish(lcd_msg2)
        rospy.sleep(0.2)
        lcd_pub3.publish(lcd_msg3)
        speak_pub.publish(speech_msg)
        rospy.sleep(0.2)
        lcd_pub4.publish(lcd_msg4)
        rospy.sleep(0.2)

        rospy.sleep(5)
