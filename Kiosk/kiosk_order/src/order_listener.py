#!/usr/bin/env python
import rospy
from std_msgs.msg import String

def callback(data):
    rospy.loginfo("주문 수신: %s", data.data)

def listener():
    rospy.init_node('order_listener', anonymous=True)
    rospy.Subscriber('/order_topic', String, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
