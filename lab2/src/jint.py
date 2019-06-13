#!/usr/bin/env python


# read a library
from lab2.srv import params
import rospy
from sensor_msgs.msg import JointState
from std_msgs.msg import Header

# frequency declaration
f = 50.0

def methodInterpolation(method, start, end, temp, it):
	if (method == "Linear"):
		pos = []
		pos.append(start[0]+(end[0]-start[0])/temp*it) 
	       	pos.append(start[1]+(end[1]-start[1])/temp*it) 
		pos.append(start[2]+(end[2]-start[2])/temp*it) 

	return pos


def jintFunction(params):
    
    if params.time <= 0:
        print ("Wrong time value")
        return -1

    # declaration of start and end point 
    start = [0, 0, 0]
    end = [float(params.j1), float(params.j2), float(params.j3)]

    temp = f * params.time
    # loop to calculate actual position using a specific interpolation method
    for it in range(0,int(temp)):
	try:
 		pos = methodInterpolation("Linear", start=start, end=end, temp=temp, it=it)
		print(pos)
	except: 
		print("definition of the function is wrong!")

	rate = rospy.Rate(f)
	
	# create a new JoinState
        newJS = JointState()
        newJS.header = Header()
        newJS.header.stamp = rospy.Time.now()
	newJS.header.frame_id = 'base_link'
	newJS.name = ['link1_join1', 'join2_link3', 'join3_link4']
        newJS.position = [-pos[0], pos[1], pos[2]]
        newJS.velocity = []
	newJS.effort = []

        pub.publish(newJS)
        rate.sleep()

    current_time = 0
    return (str(params.j1)+" "+str(params.j2)+" "+str(params.j3))


if __name__ == '__main__':
    rospy.init_node('jint_node')
    pub = rospy.Publisher('joint_states', JointState, queue_size=10)
    service = rospy.Service('jint', params, jintFunction)
    rospy.spin()
