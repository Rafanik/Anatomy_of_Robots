#! /usr/bin/python

# library to connect to rospy
import rospy

# library to json file
import json

# library to KDL
import PyKDL as kdl

# library to packages
from visualization_msgs.msg import Marker
from sensor_msgs.msg import *
from geometry_msgs.msg import *
from tf.transformations import *

def callback(data):
    # <PyKDL.Chain object at 0x7f29da463640>
    kdlChain = kdl.Chain()  
    
    # frame
    
    #[[      1,           0,           0;
    #        0,           1,           0;
    #        0,           0,           1]
    #[       0,           0,           0]]

    frame = kdl.Frame()

    poseR = PoseStamped()

    with open('in.json', 'r') as file:
        # we open our file and read parameters
        params = json.loads(file.read())

 
    fRow = params["firstRow"]
    sRow = params["secondRow"]
    tRow = params["thirdRow"]

	# in .json file: 	a,	 d,	 alpha,	 theta
	# in frame.DH function:	a, 	alpha,	 d,	 theta


    kdlChain.addSegment(kdl.Segment(kdl.Joint(kdl.Joint.TransZ), frame.DH(sRow[0], 0, fRow[1], fRow[3])))
    kdlChain.addSegment(kdl.Segment(kdl.Joint(kdl.Joint.RotZ), frame.DH(tRow[0], 0, 0, sRow[3])))


    # 0.5 because the length of the end elements
    kdlChain.addSegment(kdl.Segment(kdl.Joint(kdl.Joint.RotZ), frame.DH(0.5, 0, 0, 0)))

    jointPos = kdl.JntArray(kdlChain.getNrOfJoints())
      
    jointPos[0] = data.position[0] 
    jointPos[1] = data.position[1]
    jointPos[2] = data.position[2]
    
    forvKin = kdl.ChainFkSolverPos_recursive(kdlChain)
    eeFrame = kdl.Frame() 
    forvKin.JntToCart(jointPos, eeFrame)

    quaternion = eeFrame.M.GetQuaternion()

    poseR.header.frame_id = 'base_link'
    poseR.header.stamp = rospy.Time.now()


    poseR.pose.position.x = eeFrame.p[0]
    poseR.pose.position.y = eeFrame.p[1]
    poseR.pose.position.z = eeFrame.p[2]

    poseR.pose.orientation.x = quaternion[0]
    poseR.pose.orientation.y = quaternion[1]
    poseR.pose.orientation.z = quaternion[2]
    poseR.pose.orientation.w = quaternion[3]

    publisher.publish(poseR)


def kdl_listener():
    rospy.init_node('KDL_DKIN', anonymous = False)

    rospy.Subscriber("joint_states", JointState , callback)

    rospy.spin()

if __name__ == '__main__':
    publisher = rospy.Publisher('kdl', PoseStamped, queue_size=10)

    # laczenie z modelem
    try:
        kdl_listener()        
    except rospy.ROSInterruptException:
        pass
