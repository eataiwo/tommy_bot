#!/usr/bin/env python

import RPi.GPIO as GPIO
import socket
import rospy
import signal, sys
from flask import Flask, render_template, request, redirect, url_for, make_response
from std_msgs.msg import Float64, String, Bool

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

# Get server ip
# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.connect(("8.8.8.8", 80))
# server_ip = s.getsockname()[0]
# s.close()

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', server_ip=server_ip, speed=speed_msg.data)

@app.route('/forward')
def forward():
    direction_msg.data = 'forward'
    direction_publisher.publish(direction_msg)
    rospy.loginfo('button working')
    if not drive_msg.data:
        drive_msg.data = True
        drive_publisher.publish(drive_msg)
    return "nothing"

@app.route('/backward')
def backward():
    direction_msg.data = 'backward'
    direction_publisher.publish(direction_msg)
    rospy.loginfo('button working')
    if not drive_msg.data:
        drive_msg.data = True
        drive_publisher.publish(drive_msg)
    return "nothing"

@app.route('/left')
def left():
    direction_msg.data = 'left'
    direction_publisher.publish(direction_msg)
    rospy.loginfo('button working')
    if not drive_msg.data:
        drive_msg.data = True
        drive_publisher.publish(drive_msg)
    return "nothing"

@app.route('/right')
def right():
    direction_msg.data = 'right'
    direction_publisher.publish(direction_msg)
    rospy.loginfo('button working')
    if not drive_msg.data:
        drive_msg.data = True
        drive_publisher.publish(drive_msg)
    return "nothing"

@app.route('/cw')
def cw():
    direction_msg.data = 'cw'
    direction_publisher.publish(direction_msg)
    rospy.loginfo('button working')
    if not drive_msg.data:
        drive_msg.data = True
        drive_publisher.publish(drive_msg)
    return "nothing"

@app.route('/ccw')
def ccw():
    direction_msg.data = 'ccw'
    direction_publisher.publish(direction_msg)
    rospy.loginfo('button working')
    if not drive_msg.data:
        drive_msg.data = True
        drive_publisher.publish(drive_msg)
    return "nothing"

@app.route('/stop')
def stop():
    drive_msg.data = False
    drive_publisher.publish(drive_msg)
    rospy.loginfo('button working')
    return "nothing"

@app.route('/speed_up')
def speed_up():
    speed_msg.data += 5
    speed_publisher.publish(speed_msg)
    rospy.loginfo('button working')
    return "nothing"

@app.route('/speed_down')
def speed_down():
    speed_msg.data -= 5
    speed_publisher.publish(speed_msg)
    rospy.loginfo('button working')
    return "nothing"

def signal_handler(signal, frame):
    rospy.signal_shutdown("end")
    sys.exit(0)
    
signal.signal(signal.SIGINT,signal_handler)

app.run(debug=True, host='0.0.0.0', port=8000, threaded=True)
