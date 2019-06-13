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
# length of the manipulator's tip
end_len=0.5
# matrice for the translation of tip
tz = translation_matrix((0, 0, 0))
rz = rotation_matrix(0, zaxis)
tx = translation_matrix((end_len, 0, 0))
rx = rotation_matrix(0, xaxis)
end_matrice = concatenate_matrices(tx, rx, tz, rz)


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
    start = [0, 0, 0]
    end = [float(params.j1), float(params.j2), float(params.j3)]

	
    temp = f * params.time
	
    for it in range(0, int(temp)+1):
	pos = methodInterpolation("Linear", start, end, temp, it)
	mainMatrix = translation_matrix((0, 0, 0))
    
	matrices = {}
	
		
	with open('in.json') as file:
		parameters = json.loads(file.read())

		matrices = {}
		for key in parameters.keys():
			a, d, al, th = parameters[key]
			al, a, d, th = float(al), float(a), float(d), float(th)

			# applying changes published by joint_state_publisher
			if key == 'firstRow':
				tz = translation_matrix((0, 0, d+pos[0]))
				rz = rotation_matrix(th, zaxis)
            
			if key == 'secondRow':
				tz = translation_matrix((0, 0, d))
				rz = rotation_matrix(th+pos[1], zaxis)
			if key == 'thirdRow' :
				tz = translation_matrix((0, 0, d))
				rz = rotation_matrix(th+pos[2], zaxis)

			# creating matrix
			tx = translation_matrix((a, 0, 0))
			rx = rotation_matrix(al, xaxis)
			matrices[key] = concatenate_matrices(tx, rx, tz, rz)
            
		# multiplication of matrices
		for key in sorted(parameters.keys()):
			mainMatrix = concatenate_matrices(mainMatrix,matrices[key])
 

		mainMatrix = concatenate_matrices(mainMatrix,end_matrice)
     
		# counting the parameters from the mainMatrix
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
