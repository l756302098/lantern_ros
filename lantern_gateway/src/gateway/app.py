#!/usr/bin/env python
#coding=utf-8
import rospy
from server import GateServer
from tornado import ioloop, gen, iostream
from tornado.netutil import bind_sockets
from logic import Logic
from .bridge import create_bridge

class gate_node():
    def __init__(self):
        # init node
        rospy.init_node('lantern_gateway_node')
        # load parameters
        params = rospy.get_param("~", {})
        print("load params:")
        print(params)
        bridge_params = params.get("bridge", [])
        print(bridge_params)
        # start server
        sockets = bind_sockets(GateServer.PORT)
        server = GateServer()
        server.add_sockets(sockets)
        # register shutdown callback and spin
        rospy.on_shutdown(self.cleanup)
        server.logic = Logic()
        # configure bridges
        bridges = []
        for bridge_args in bridge_params:
            print(bridge_args)
            bridges.append(create_bridge(**bridge_args))

        # hang
        print("ioloop start")
        ioloop.IOLoop.current().start()
        print("node spin")

    def cleanup(self):
        print "Shutting down gateway node."
        ioloop.IOLoop.current().stop()