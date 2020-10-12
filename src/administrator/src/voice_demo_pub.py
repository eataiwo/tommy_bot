#!/usr/bin/env python


import rospy
from std_msgs.msg import String

speech = String()

if __name__ == '__main__':
    rospy.init_node('voice_demo_pub')
    voice_pub = rospy.Publisher('/voice/speak', String, queue_size=10)
    rospy.sleep(0.2)

    test_phrases = ['Testing', 'Hi I am tommy', 'I am now ready for an adventure', 'Stand by', 'Alert', '5 4 3 2 1',
                    'The time is 4:15 pm', 'Obstacle detected', 'Hello Tee Jay', ' Once upon a time',
                    "Sittin in the morning sun I'll be sittin' when the evening come Watching the ships roll in"
                    " And I'll watch 'them roll away again, yeah I'm sittin' on the dock of the bay"]

    while voice_pub.get_num_connections() == 0:
        rospy.sleep(0.1)

    for i in test_phrases:
        speech.data = i
        voice_pub.publish(speech)
        rospy.sleep(3)

    signoff = 'Speech testing is finished'
    speech.data = signoff
    voice_pub.publish(speech)
    rospy.loginfo(signoff)
