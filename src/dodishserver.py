#! /usr/bin/env python

import roslib
roslib.load_manifest('my_cv_pkg')
import rospy
import actionlib

from chores.msg import DoDishesAction

class DoDishesServer:
	def __init__(self):
		self.server = actionlib.SimpleActionServer('do_dishes', DoDishesAction, self.execute, False)
		self.server.start()
	
	def execute(self, goal):
		self.server.set_succeeded()

if __name__ == '__main__':
	rospy.init_node('do_dishes_server')
	server = DoDishesServer()
	rospy.spin()
