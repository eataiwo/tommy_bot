#!/usr/bin/python

#####################################################################
# Author: Jeferson Menegazzo                                        #
# Year: 2020                                                        #
# License: MIT                                                      #
#####################################################################

import sys
# sys.path.append("")

import rospy
from std_msgs.msg import Float64, Header
from numpy import deg2rad
from sensor.msgs.msg import Imu, MagneticField, Temperature
from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250

# For covariance I would need to implement an Extended Kalman Filter or something.

g =  9.80665

# Create
mpu = MPU9250(
    address_ak=AK8963_ADDRESS,
    address_mpu_master=MPU9050_ADDRESS_68,  # In 0x68 Address
    address_mpu_slave=None,
    bus=1,
    gfs=GFS_1000,
    afs=AFS_8G,
    mfs=AK8963_BIT_16,
    mode=AK8963_MODE_C100HZ)


# Configure
mpu.configure()  # Apply the settings to the registers.

# Calibrate
# Before calibration starts send a message to lcd screen warning calibration is happening
#mpu.calibrate() # Calibrate sensors
#mpu.configure() # The calibration function resets the sensors, so you need to reconfigure them
# Add message that calibration of IMU is done


# TODO: Delete once I am happy with script
# Get Calibration
# abias = mpu.abias # Get the master accelerometer biases
# gbias = mpu.gbias # Get the master gyroscope biases
# magScale = mpu.magScale # Get magnetometer soft iron distortion
# mbias = mpu.mbias # Get magnetometer hard iron distortion

# print("|.....MPU9250 in 0x68 Biases.....|")
# print("Accelerometer", abias)
# print("Gyroscope", gbias)
# print("Magnetometer SID", magScale)
# print("Magnetometer HID", mbias)
# print("\n")


# Show Values
# while True:
#     print("|.....MPU9250 in 0x68 Address.....|")
#     print("Accelerometer", mpu.readAccelerometerMaster())
#     print("Gyroscope", mpu.readGyroscopeMaster())
#     print("Magnetometer", mpu.readMagnetometerMaster())
#     print("Temperature", mpu.readTemperatureMaster())
#     print("\n")
#
#     time.sleep(1)

rospy.init_node('MPU9250')
rate = rospy.Rate(60)

imu_msg = Imu()
mag_msg = MagneticField()
temp_msg = Temperature()
header = Header()

temp_pub = rospy.Publisher('sensors/imu_temperature', Temperature, queue_size=10)
imu_pub = rospy.Publisher('imu/data_raw', Imu, queue_size=10)
mag_pub = rospy.Publisher('imu/mag', MagneticField, queue_size=10)

while not rospy.is_shutdown():

    header.stamp = rospy.Time.now()
    header.frame_id = 'tommy'

    imu_msg.linear_acceleration= mpu.readAccelerometerMaster*g
    imu_msg.angular_velocity = deg2rad(mpu.readGyroscopeMaster())
    mag_msg.magnetic_field = mpu.readMagnetometerMaster()
    temp_msg.temperature = mpu.readTemperatureMaster()

    imu_msg.header = mag_msg.header = temp_msg.header = header

    temp_pub.publish(temp_msg)
    imu_pub.publish(imu_msg)
    mag_pub.publish(mag_msg)

    rate.sleep()

