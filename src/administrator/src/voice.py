#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import simpleaudio as sa
from picotts import PicoTTS

picotts = PicoTTS()
picotts.voice = 'en-GB'


def cb_speak(msg):
    wav = picotts.synth_wav(msg)
    wav = sa.WaveObject(wav, 2, 2, 8000)
    another_obj = wav.play()
    another_obj.wait_done()


if __name__ == '__main__':
    rospy.init_node('voice')
    voice_sub = rospy.Subscriber('/voice/speak', String, cb_speak, queue_size=20)

    rospy.spin()


# Example TODO: Delete when happy with script
# wav = picotts.synth_wav('omelette du fromage')
# play_obj = sa.play_buffer(wav, 2, 2, 8000)
# play_obj.wait_done()

# picotts.voice = 'en-GB'
# wav = picotts.synth_wav('omelette du fromage')
# wav = sa.WaveObject(wav, 2, 2, 8000)
# another_obj = wav.play()
# another_obj.wait_done()
