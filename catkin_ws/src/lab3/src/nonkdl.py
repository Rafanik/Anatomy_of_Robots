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

#zdefiniowanie osi
xaxis, yaxis, zaxis = (1, 0, 0), (0, 1, 0), (0, 0, 1)

#przesuniecie koncowki w osi x od ostatniego czlonu
end_len=0.5
#macierz przesuniecia koncowki
tz = translation_matrix((0, 0, 0))
rz = rotation_matrix(0, zaxis)
tx = translation_matrix((end_len, 0, 0))
rx = rotation_matrix(0, xaxis)
end_matrice = concatenate_matrices(tx, rx, tz, rz)

def callback(data):
    mainMatrix = translation_matrix((0, 0, 0))
 

    #wczytanie parametrow z tablicy dh
    with open('in.json') as file:
        params = json.loads(file.read())
        matrices = {}
        for key in params.keys():
            a, d, alpha, theta = params[key]
            alpha, a, d, theta = float(alpha), float(a), float(d), float(theta)

            #modyfikacja odpowiednich macierzy relacji o zmiane kata z joint_state_publishera
            if key == 'firstRow':
                tz = translation_matrix((0, 0, d+data.position[0]))
                rz = rotation_matrix(theta, zaxis)
            
            if key == 'secondRow':
                tz = translation_matrix((0, 0, d))
                rz = rotation_matrix(theta+data.position[1], zaxis)
            if key == 'thirdRow' :
                tz = translation_matrix((0, 0, d))
                rz = rotation_matrix(theta+data.position[2], zaxis)

            #stworzenie macierzy
            tx = translation_matrix((a, 0, 0))
            rx = rotation_matrix(alpha, xaxis)
            matrices[key] = concatenate_matrices(tx, rx, tz, rz)
                
    # wymnozenie macierzy
    for key in sorted(params.keys()):
        mainMatrix = concatenate_matrices(mainMatrix,end_matrice)
 
    
    # wyciagniecie odpowiednich parametrow z macierzy jednorodnej
    x, y, z = translation_from_matrix(mainMatrix)
    
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

    # opublikowanie pozycji na temat
    publisher.publish(poseR)


def nonkdl_listener():

    rospy.init_node('NONKDL_DKIN', anonymous = False)

    rospy.Subscriber("joint_states", JointState , callback)

    rospy.spin()

if __name__ == '__main__':

    publisher = rospy.Publisher('n_k_axes', PoseStamped, queue_size=10)

    try:
        nonkdl_listener()        
    except rospy.ROSInterruptException:
        pass

