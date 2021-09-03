#!/usr/bin/env python
#coding=utf-8
import rospy
from server import GateServer
from tornado import ioloop, gen, iostream
from logic import Logic

class gate_node():
    def __init__(self):
        # init node
        rospy.init_node('lantern_gateway_node')
        # load parameters
        params = rospy.get_param("~", {})
        print("load params:")
        print(params)
        bridge_params = params.get("bridge", [])
        # start server
        server = GateServer()
        server.listen(9091)
        server.start()
        rospy.on_shutdown(self.cleanup)
        server.logic = Logic()
        # Hold on
        print("ioloop start")
        ioloop.IOLoop.current().start()
        print("node spin")
        # register shutdown callback and spin
        #rospy.spin()

    def cleanup(self):
        print "Shutting down gateway node."
        ioloop.IOLoop.current().stop()