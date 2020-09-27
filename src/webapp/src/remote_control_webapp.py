#!/usr/bin/env python

import RPi.GPIO as GPIO
import rospy
import signal, sys
from flask import Flask, render_template, request, redirect, url_for, make_response, Response
from std_msgs.msg import Float64, String, Bool
from camera import Camera

app = Flask(__name__)

# Setup ROS node and publishers
rospy.init_node('webapp_remote_controller')
speed_publisher = rospy.Publisher('/powertrain/speed', Float64, queue_size=10)
direction_publisher = rospy.Publisher('/powertrain/direction', String, queue_size=10)
drive_publisher = rospy.Publisher('/powertrain/drive', Bool, queue_size=10)

speed_msg = Float64()
speed_msg.data = 80
direction_msg = String()
drive_msg = Bool()
drive_msg.data = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/forward')
def forward():
    direction_msg.data = 'forward'
    direction_publisher.publish(direction_msg)
    # rospy.loginfo('button working')  # For debugging
    if not drive_msg.data:
        drive_msg.data = True
        drive_publisher.publish(drive_msg)
    return "nothing"

@app.route('/backward')
def backward():
    direction_msg.data = 'backward'
    direction_publisher.publish(direction_msg)
    if not drive_msg.data:
        drive_msg.data = True
        drive_publisher.publish(drive_msg)
    return "nothing"

@app.route('/left')
def left():
    direction_msg.data = 'left'
    direction_publisher.publish(direction_msg)
    if not drive_msg.data:
        drive_msg.data = True
        drive_publisher.publish(drive_msg)
    return "nothing"

@app.route('/right')
def right():
    direction_msg.data = 'right'
    direction_publisher.publish(direction_msg)
    if not drive_msg.data:
        drive_msg.data = True
        drive_publisher.publish(drive_msg)
    return "nothing"

@app.route('/cw')
def cw():
    direction_msg.data = 'cw'
    direction_publisher.publish(direction_msg)
    if not drive_msg.data:
        drive_msg.data = True
        drive_publisher.publish(drive_msg)
    return "nothing"

@app.route('/ccw')
def ccw():
    direction_msg.data = 'ccw'
    direction_publisher.publish(direction_msg)
    if not drive_msg.data:
        drive_msg.data = True
        drive_publisher.publish(drive_msg)
    return "nothing"

@app.route('/stop')
def stop():
    drive_msg.data = False
    drive_publisher.publish(drive_msg)
    return "nothing"

@app.route('/speed_up')
def speed_up():
    speed_msg.data += 5
    speed_publisher.publish(speed_msg)
    return "nothing"

@app.route('/speed_down')
def speed_down():
    speed_msg.data -= 5
    speed_publisher.publish(speed_msg)
    return "nothing"

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

#TODO: See if node shutsdown without this and if the arguments signal and frame are required
def signal_handler(signal, frame):
    rospy.signal_shutdown("end")
    sys.exit(0)
    
signal.signal(signal.SIGINT,signal_handler)

app.run(debug=True, host='0.0.0.0', port=8000)

