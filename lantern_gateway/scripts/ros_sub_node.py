#!/usr/bin/env python
#coding=utf-8
import rospy
# from gateway.server

if __name__ == '__main__':    
    try:
        rospy.init_node('ros_sub_node')
        rate = rospy.Rate(20) # 20hz
        while not rospy.is_shutdown():
            rate.sleep()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        rospy.shutdown()
    except rospy.ROSInterruptException:
        rospy.shutdown()