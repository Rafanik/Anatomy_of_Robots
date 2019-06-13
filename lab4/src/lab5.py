#!/usr/bin/env python

import rospy
from lab2.srv import params
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
import json
from sensor_msgs.msg import *
from tf.transformations import *
from visualization_msgs.msg import Marker
from geometry_msgs.msg import PoseStamped
import math


# frequency declaration
f = 50.0

def jintFunction(data):
    
	rate = rospy.Rate(f)

	r14 = float(data.pose.position.x)
	r24 = float(data.pose.position.y)
	r34 = float(data.pose.position.z)
	A3 = 2.0
	E = 0.5



	# theta2
	 
	#theta2_sol = 2*math.atan((2*A3*r24 + (- A3**4 + 2*A3**2*E**2 + 2*A3**2*r14**2 + 2*A3**2*r24**2 - E**4 + 2*E**2*r14**2 + 2*E**2*r24**2 - r14**4 - 2*r14**2*r24**2 - r24**4)**(1/2))/(A3**2 + 2*A3*r14 - E**2 + r14**2 + r24**2))
	theta2_sol = 2.0*math.atan((2*A3*r24 - (-A3**4 + 2*A3**2*E**2 + 2*A3**2*r14**2 + 2*A3**2*r24**2 - E**4 + 2*E**2*r14**2 + 2*E**2*r24**2 - r14**4 - 2*r14**2*r24**2 - r24**4)**(0.5))/(A3**2 + 2*A3*r14 - E**2 + r14**2 + r24**2))
	 

	# theta3

	#theta3_sol = -2*math.atan(((A3**2 + 2*A3*E + E**2 - r14**2 - r24**2)*(- A3**2 + 2*A3*E - E**2 + r14**2 + r24**2))**(1/2)/(- A3**2 + 2*A3*E - E**2 + r14**2 + r24**2))
	theta3_sol = 2.0*math.atan(((A3**2 + 2*A3*E + E**2 - r14**2 - r24**2)*(- A3**2 + 2*A3*E - E**2 + r14**2 + r24**2))**0.5/(- A3**2 + 2*A3*E - E**2 + r14**2 + r24**2))

	# D1

	D1_sol = r34

	# create a new JoinState
	newJS = JointState()
	newJS.header = Header()
	newJS.header.stamp = rospy.Time.now()
	newJS.header.frame_id = 'base_link'
	newJS.name = ['link1_join1', 'join2_link3', 'join3_link4']
	newJS.position = [D1_sol-1, theta2_sol, theta3_sol]
	newJS.velocity = []
	newJS.effort = []

	pub.publish(newJS)
	rate.sleep()
	print(data.pose.position)





if __name__ == '__main__':
    rospy.init_node('jint_node')
    rospy.Subscriber("oint", PoseStamped, jintFunction)
    pub = rospy.Publisher('joint_states', JointState, queue_size=10)
    service = rospy.Service('jint', params, jintFunction)
    rospy.spin()


