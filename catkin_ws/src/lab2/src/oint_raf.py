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


# frequency declaration
f = 10.0

xaxis, yaxis, zaxis = (1, 0, 0), (0, 1, 0), (0, 0, 1)



def methodInterpolation(method, start, end, temp, it):
	if (method == "Linear"):
		pos = []
		pos.append(start[0]+(end[0]-start[0])/temp*it) 
	    	pos.append(start[1]+(end[1]-start[1])/temp*it) 
		pos.append(start[2]+(end[2]-start[2])/temp*it) 
	return pos


def ointFunction(params):
    if params.time <= 0:
        print ("Wrong time value")
        return -1


    # declaration of start and end point 
    
    start = [0, 0, 0,]
    end = [float(params.j1), float(params.j2), float(params.j3)]

	
    temp = f * params.time
    x=0
    y=0
    z=0
	
    for it in range(0, int(temp)+1):
	pos = methodInterpolation("Linear", start, end, temp, it)
	mainMatrix = translation_matrix((0, 0, 0))
    
	matrices = {}
	
	# counting the parameters from the mainMatrix
	x=pos[0]
	y=pos[1]
	z=pos[2]
	
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
	rate = rospy.Rate(50)
	rate.sleep()
	print(pos)

    current_time = 0
    return (str(params.j1)+" "+str(params.j2)+" "+str(params.j3))


if __name__ == "__main__":
    rospy.init_node('oint_node')
    publisher = rospy.Publisher('oint', PoseStamped , queue_size=10)
    s = rospy.Service('oint', params, ointFunction)
    rospy.spin()
