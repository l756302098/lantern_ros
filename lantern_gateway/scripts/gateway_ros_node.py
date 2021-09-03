#!/usr/bin/env python
#coding=utf-8
import rospy
from gateway.app import gate_node

if __name__ == '__main__':        
    try:
        gate = gate_node()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        rospy.shutdown()
    except rospy.ROSInterruptException:
        rospy.shutdown()