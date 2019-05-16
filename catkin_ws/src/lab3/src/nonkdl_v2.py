#! /usr/bin/python

import rospy
import json
from sensor_msgs.msg import *
from geometry_msgs.msg import *
from tf.transformations import *
from numpy import * 
from math import sin, cos

# defining axes
xaxis, yaxis, zaxis = (1, 0, 0), (0, 1, 0), (0, 0, 1)

# length of the manipulator's tip
E=0.5
# matrice for the translation of tip

def callback(data):
    mainMatrix = translation_matrix((0, 0, 0))

    # reading dh table parameters
    with open('in.json') as file:
        params = json.loads(file.read())
	matrices = {}
	

	theta2 = float(params["secondRow"][3])
	theta3 = float(params["thirdRow"][3])
	D1 = float(params["firstRow"][1])
	A2 = float(params["secondRow"][0])
	A3 = float(params["thirdRow"][0])

    mainMatrix = array([[cos(theta2+data.position[1])*cos(theta3+data.position[2]) - sin(theta2+data.position[1])*sin(theta3+data.position[2]), - cos(theta2+data.position[1])*sin(theta3+data.position[2]) - cos(theta3+data.position[2])*sin(theta2+data.position[1]), 0, A2 + E*(cos(theta2+data.position[1])*cos(theta3+data.position[2]) - sin(theta2+data.position[1])*sin(theta3+data.position[2])) + A3*cos(theta2+data.position[1])],
[ cos(theta2+data.position[1])*sin(theta3+data.position[2]) + cos(theta3+data.position[2])*sin(theta2+data.position[1]),   cos(theta2+data.position[1])*cos(theta3+data.position[2]) - sin(theta2+data.position[1])*sin(theta3+data.position[2]), 0,      E*(cos(theta2+data.position[1])*sin(theta3+data.position[2]) + cos(theta3+data.position[2])*sin(theta2+data.position[1])) + A3*sin(theta2+data.position[1])],
[                                                 0,                                                   0, 1,                                                                          D1+data.position[0]],
[ 0,  0, 0, 1]])

    
    x , y , z = translation_from_matrix(mainMatrix)
    
    poseR = PoseStamped()
    poseR.header.frame_id = "base_link"
    poseR.header.stamp = rospy.Time.now()
    poseR.pose.position.x = x
    poseR.pose.position.y = y
    poseR.pose.position.z = z
    
    xq, yq, zq, wq = quaternion_from_matrix(mainMatrix)

    poseR.pose.orientation.x = xq
    poseR.pose.orientation.y = yq
    poseR.pose.orientation.z = zq
    poseR.pose.orientation.w = wq

    # publishing the position via proper topic
    publisher.publish(poseR)


def nonkdl_listener():

    rospy.init_node('NONKDL_DKIN', anonymous = False)

    rospy.Subscriber("joint_states", JointState , callback)

    rospy.spin()

if __name__ == '__main__':

    publisher = rospy.Publisher('nonkdl', PoseStamped, queue_size=10)

    try:
	    nonkdl_listener()        
    except rospy.ROSInterruptException:
	pass