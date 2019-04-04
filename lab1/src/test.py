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
    
	# ustawienie czestotliwosci publikowania
	rate = rospy.Rate(10) # 10hz

	# pobranie parametrow z serwera parametrow - klawisze sterowania
	FORWARD = rospy.get_param("forward")
	BACKWARD = rospy.get_param("backward")
	TURNLEFT = rospy.get_param("turnLeft")
	TURNRIGHT = rospy.get_param("turnRight")

	twist = Twist()

	while not rospy.is_shutdown():

		# pobranie wartosci wcisnietego klawisza
		letter = getchar()

		# pobranie aktualnych wartosci predkosci liniowej i katowej z serwera parametrow
		LINVELOCITY = rospy.get_param("linVelocity")
		ANGVELOCITY = rospy.get_param("angVelocity")

		# ustawienie odpowiednich predkosci w zaleznosci od wartosci wcisnietego klawisza
		if letter == FORWARD:
			twist.linear.x = LINVELOCITY
			twist.angular.z = 0.0
		elif letter == TURNLEFT:
			twist.linear.x  = 0.0
			twist.angular.z = ANGVELOCITY
		elif letter == TURNRIGHT:
			twist.linear.x  = 0.0
			twist.angular.z = -ANGVELOCITY
		elif letter == BACKWARD:
			twist.linear.x  = -LINVELOCITY
			twist.angular.z = 0.0

		# publikowanie wiadomosci
		pub.publish(twist)
		rate.sleep()


if __name__ == '__main__':
    try:
        move()
    except rospy.ROSInterruptException:
	pass