#!/usr/bin/env python

import rospy
from std_msgs.msg import String, Bool, Float64

speed_publisher = rospy.Publisher('/powertrain/speed', Float64, queue_size=10)
direction_publisher = rospy.Publisher('/powertrain/direction', String, queue_size=10)
distance_publisher = rospy.Publisher('/powertrain/distance', Float64, queue_size=10)
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
    distance_publisher.publish(distance_msg)
    drive_publisher.publish(drive_msg)
    
    rospy.loginfo('Published speed, distance and drive state')

    for i in test_directions:
        direction_msg.data = i
        direction_publisher.publish(direction_msg)
        speed_publisher.publish(speed_msg)
        distance_publisher.publish(distance_msg)
        drive_publisher.publish(drive_msg)
        rospy.loginfo(f'Published direction {direction_msg.data}')
        rospy.sleep(5.)
