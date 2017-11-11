#/use/bin/env python
import sys
import rospy, actionlib
from move_base_msgs.msg import *
from opencv_apps.msg import RotatedRectStamped
from geometry_msgs.msg import Point
def cb(msg):
	print msg.rect
	if msg.rect.center.x != 0. and msg.rect.center.y != 0.:
		pos = [-3,3]
		goal = MoveBaseGoal()
		goal.target_pose.header.stamp = rospy.Time.now()
		goal.target_pose.header.frame_id = "/map"
		goal.target_pose.pose.position.x = pos[0];
		goal.target_pose.pose.position.y = pos[1];
		goal.target_pose.pose.orientation.w = 1
		print goal
		client.send_goal(goal)
		sys.exit()
if __name__ == '__main__':
	try:
		rospy.init_node('send_goal', anonymous=True)
		client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
		client.wait_for_server()
		
		rospy.Subscriber('/camshift/track_box', RotatedRectStamped, cb)
		#print client.wait_for_result()
		rospy.spin()
	except rospy.ROSInterruptException: pass
