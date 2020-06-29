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
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
server_ip = s.getsockname()[0]
s.close()

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', server_ip=server_ip)


@app.route('/<changepin>', methods=['POST'])
def reroute(changepin):
    changepin = int(changepin)
    if changepin == 1:
        direction_msg.data = 'left'
    elif changepin == 2:
        direction_msg.data = 'forward'
    elif changepin == 3:
        direction_msg.data = 'right'
    elif changepin == 4:
        direction_msg.data = 'backward'
    elif changepin == 5:
        drive_msg.data = False
        drive_publisher.publish(drive_msg)
    elif changepin == 6:
        direction_msg.data = 'tots_cw'
    elif changepin == 7:
        direction_msg.data = 'tots_ccw'
    elif changepin == 8:
        speed_msg.data -= 5
    elif changepin == 9:
        speed_msg.data += 5
    else:
        print("Wrong command")
        
    direction_publisher.publish(direction_msg)
    speed_publisher.publish(speed_msg)
    if not drive_msg.data and changepin != 5:
        drive_msg.data = True
        drive_publisher.publish(drive_msg)   
    response = make_response(redirect(url_for('index')))
    return response

def signal_handler(signal, frame):
    rospy.signal_shutdown("end")
    sys.exit(0)
    
signal.signal(signal.SIGINT,signal_handler)

app.run(debug=True, host='0.0.0.0', port=8000)
