#!/usr/bin/env python

# import potrzebnych pakietow
from click import getchar
import rospy
from geometry_msgs.msg import Twist 

def move():
	'''
	funkcja odpowiadajaca za sterowanie
	'''
    
	# stworzenie publishera
	pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    
	# inicjacja wezla
	rospy.init_node('lab1')
    
	rate = rospy.Rate(10) # 10hz

	FORWARD = rospy.get_param("forward")
	BACKWARD = rospy.get_param("backward")
	TURNLEFT = rospy.get_param("turnLeft")
	TURNRIGHT = rospy.get_param("turnRight")

	twist = Twist()

	while not rospy.is_shutdown():
		letter = getchar()

		if letter == FORWARD:
			twist.linear.x = 1.0
			twist.angular.z = 0.0
		elif letter == TURNLEFT:
			twist.linear.x  = 0.0
			twist.angular.z = 1.0
		elif letter == TURNRIGHT:
			twist.linear.x  = 0.0
			twist.angular.z = -1.0
		elif letter == BACKWARD:
			twist.linear.x  = -1.0
			twist.angular.z = 0.0

		# publikowanie wiadomosci
		pub.publish(twist)
		rate.sleep()


if __name__ == '__main__':
    try:
        move()
    except rospy.ROSInterruptException:
	pass
