#!/usr/bin/env python
#coding=utf-8
from tornado import gen, iostream
from tornado.ioloop import IOLoop
from tornado.tcpserver import TCPServer
from server import GateServer

class Logic():

    def __init__(self):
        IOLoop.current().spawn_callback(self.receive_msg)

    def input(self,data):
        """
        receive json data
        """
        print("input:",data)
        GateServer.send_q.put((1, 'medium-priority item'))
        return None

    @gen.coroutine
    def receive_msg(self):
        while True:
            try:
                print("read from queue")
                while not GateServer.receive_q.empty():
                    print("size:",GateServer.receive_q.qsize())
                    item = yield GateServer.receive_q.get()
                    if item is not None:
                        print(item[0],item[1])
                    #print(GateServer.send_q.get_nowait())
                    # msg_tupe = GateServer.send_q.get_nowait()
            except:
                print("receive error")
            yield gen.sleep(1.0)
    
    def resolveJson(self):
        """
        receive json data
        """
        pass