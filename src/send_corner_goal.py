#/use/bin/env python

import rospy, actionlib
from move_base_msgs.msg import *

if __name__ == '__main__':
	try:
		rospy.init_node('send_goal', anonymous=True)
		client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
		client.wait_for_server()

		for pos in [[3,3],[3,-3],[-3,-3],[-3,3]]:
			goal = MoveBaseGoal()
			goal.target_pose.header.stamp = rospy.Time.now()
			goal.target_pose.header.frame_id = "/map"
			goal.target_pose.pose.position.x = pos[0];
			goal.target_pose.pose.position.y = pos[1];
			goal.target_pose.pose.orientation.w = 1
			print goal
			client.send_goal(goal)
			print client.wait_for_result()
	except rospy.ROSInterruptException: pass
