#!/usr/bin/env python

import rospy
from std_msgs.msg import String, Bool, Float64

speed_publisher = rospy.Publisher('/powertrain/speed', Float64, queue_size=10)
direction_publisher = rospy.Publisher('/powertrain/direction', String, queue_size=10)
drive_publisher = rospy.Publisher('/powertrain/drive', Bool, queue_size=10)

speed_msg = Float64()
direction_msg = String()
distance_msg = Float64()
drive_msg = Bool()

speed_msg.data = 80
distance_msg.data = 0.1
drive_msg.data = True
test_directions = ['forward', 'backward', 'left', 'right']


if __name__ == '__main__':
    rospy.init_node('powertrain_demo_pub')
    
    speed_publisher.publish(speed_msg)
    
    rospy.logwarn('Robot wheels will be activated in 10s please ensure'
                   ' enough clearance between robot and surrounding obstacles'
                   ' or place robot on a platform to allow the wheels to free spin'
                   ' or disable motor power')
                   
    rospy.sleep(10)
    
    drive_publisher.publish(drive_msg)

    for i in test_directions:
        direction_msg.data = i
        direction_publisher.publish(direction_msg)
        rospy.loginfo(f'Published direction {direction_msg.data}')
        rospy.sleep(1)
        
    drive_msg.data = False
    drive_publisher.publish(drive_msg)
