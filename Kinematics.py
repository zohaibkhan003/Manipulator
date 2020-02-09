#!/usr/bin/env python

import rospy
import numpy as np
from math import pi, cos, sin, atan2, sqrt, acos
from std_msgs.msg import Float64
from collections import namedtuple

position = namedtuple('position', ['x', 'y', 'z'])
jointangle = namedtuple('jointangle', ['theta1', 'theta2', 'theta3', 'theta4'])


class OpenManipulator():
    def __init__(self):
        rospy.init_node('open_manipulator_move', anonymous=False)
        rospy.loginfo("Press CTRL + C to terminate")
        rospy.on_shutdown(self.reset)
        self.rate = rospy.Rate(10)

        self.pub_joint1 = rospy.Publisher('/open_manipulator/joint1_position/command', Float64, queue_size=10)
        self.pub_joint2 = rospy.Publisher('/open_manipulator/joint2_position/command', Float64, queue_size=10)
        self.pub_joint3 = rospy.Publisher('/open_manipulator/joint3_position/command', Float64, queue_size=10)
        self.pub_joint4 = rospy.Publisher('/open_manipulator/joint4_position/command', Float64, queue_size=10)

        # test case for forward kinematics
        joints = jointangle(pi/6, -pi/3, pi/6, pi/3)
        end_effector_position = self.forward_kinematics(joints)
        print(end_effector_position)

        # test case for inverse kinematics
        end_effector = position(0.018, 0.004, 0.222)
        joints_angle = self.inverse_kinematics(end_effector)
        print(joints_angle)

        self.move(joints)
        while not rospy.is_shutdown():
            self.rate.sleep()


    def forward_kinematics(self, joints):
        # input: joint angles in (theta1, theta2, theta3, theta4)
        # output: the position of end effector in (x, y, z)
        # hints: access to the angle of the first joint by joints.theta1
        # add your code here to complete forward kinematics
	# input: joint angles in (theta1, theta2, theta3, theta4)
        # output: the position of end effector in (x, y, z)
        # hints: access to the angle of the first joint by joints.theta1
        # add your code here to complete forward kinematics
	# Finding the M matrix and V
	I = np.matrix('1,0,0,0; 0,1,0,0; 0,0,1,0; 0,0,0,1')
	M = np.matrix('1,0,0,0.16; 0,1,0,0; 0,0,1,0.205; 0,0,0,1')
	Wvector = np.array([[0,0,1],[0,1,0],[0,1,0],[0,1,0]])
	#V = np.array [[0.0079, 0, 0.2406]]


	S1 = np.matrix('0,-1,0,0.012; 1,0,0,0; 0,0,0,0; 0,0,0,0')
	S2 = np.matrix('0,0,1,-0.077; 0,0,0,0; -1,0,0,0.012; 0,0,0,0')
	S3 = np.matrix('0,0,1,-0.205; 0,0,0,0; -1,0,0,0.036; 0,0,0,0')
	S4 = np.matrix('0,0,1,-0.205; 0,0,0,0; -1,0,0,0.16; 0,0,0,0')


	v1 = np.array([[0],[-0.012],[0]])
	v2 = np.array([[-0.077],[0],[0.012]])
	v3 = np.array([[-0.205],[0],[0.036]])
	v4 = np.array([[-0.205],[0],[0.16]])



	# Rodrigues Formula
	doubles1 = S1*S1
	R1 = I + S1*(sin(joints.theta1)) + ((1-cos(joints.theta1))*(doubles1))
	doubles2 = S2*S2
	R2 = I + S2*(sin(joints.theta2)) + ((1-cos(joints.theta2))*(doubles2))
	doubles3 = S3*S3
	R3 = I + S3*(sin(joints.theta3)) + ((1-cos(joints.theta3))*(doubles3))
	doubles4 = S4*S4
	R4 = I + S4*(sin(joints.theta4)) + ((1-cos(joints.theta4))*(doubles4))

	# V vectors
	vw1 = np.array([[-.012],[0],[0]])
	vw2 = np.array([[0.012],[0],[.077]])
	vw3 = np.array([[0.036],[-0.012],[.205]])
	vw4 = np.array([[0.16],[-0.012],[.205]])


	#T1 = (I - R1)* vw1
	#T2 = (I - R2)* vw2
	#T3 = (I - R3)* vw3	
	#T4 = (I - R4)* vw4
	
	#print(T1)
	#print(T2)
	#print(T3)
	#print(T4)


	#P1 = [M:1]

	P0 = R1*R2*R3*R4*M

	P = np.array([[0],[0],[0],[1]])

	Final = P0*P
	# Obtaining the elements
	x = Final[0][0]
	y = Final[1][0]
	z = Final[2][0]

	return position(x,y,z)


    def inverse_kinematics(self, end_effector):
        # input: the position of end effector in (x, y, z)
        # output: joint angles in (theta1, theta2, theta3, theta4)
        # hints: access to the x position of end effector by end_effector.x
        # add your code here to complete inverse kinematics
	theta1 = atan2(end_effector.x, end_effector.y)
	theta2 = theta1 - cos(end_effector.x)
	theta3 = 180-cos(end_effector.y)
	theta4 = end_effector
        return jointangle(theta1, theta2, theta3, theta4)


    def move(self, joints):
        rospy.loginfo("Manipulator demo")
        for i in range(50):
            if i >= 10:
                self.pub_joint1.publish(joints.theta1)
            if i >= 20:
                self.pub_joint2.publish(joints.theta2)
            if i >= 30:
                self.pub_joint3.publish(joints.theta3)
            if i >= 40:
                self.pub_joint4.publish(joints.theta4)
            self.rate.sleep()


    def reset(self):
        rospy.loginfo("Return to the origin")
        for i in range(50):
            if i >= 10:
                self.pub_joint4.publish(0)
            if i >= 20:
                self.pub_joint3.publish(0)
            if i >= 30:
                self.pub_joint2.publish(0)
            if i >= 40:
                self.pub_joint1.publish(0)
            self.rate.sleep()


if __name__ == '__main__':
    try:
        whatever = OpenManipulator()
    except rospy.ROSInterruptException:
        rospy.loginfo("Action terminated.")
