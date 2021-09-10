#!/usr/bin/env python
#coding=utf-8
import logging
from tornado.ioloop import IOLoop
from tornado import gen, iostream
from tornado.tcpserver import TCPServer
from tornado.queues import PriorityQueue

class GateServer( TCPServer ):

    PORT = 9091
    clients = dict()
    send_q = PriorityQueue(maxsize=100)
    receive_q = PriorityQueue(maxsize=10)

    def __init__(self):
        TCPServer.__init__(self)
        print("init gateway")
        # register ros node 
        IOLoop.current().spawn_callback(self.consumer)

    @gen.coroutine
    def consumer(self):
        while True:
            try:
                print("do something...")
                while not GateServer.send_q.empty():
                    #print("size:",GateServer.send_q.qsize())
                    item = yield GateServer.send_q.get()
                    #print(item,type(item))
                    #print(GateServer.send_q.get_nowait())
                    # msg_tupe = GateServer.send_q.get_nowait()
                    if item is not None:
                        print(item[0],item[1],type(item[1]))
                        for key,client in GateServer.clients.items():
                            print("send msg to client ",key)
                            if client is not None:
                                sb = bytes(item[1])
                                yield client.write(sb)
            except Exception as e:
                print("consumer error:",e)
            #print("yield sleep start ")
            yield gen.sleep(0.1)
            #print("yield sleep end ")

    @gen.coroutine
    def handle_stream( self, stream, address ):
        # print("get client ",address)
        ip = address[0]
        port = address[1]
        key = ip+":"+str(port)
        print(ip,port,key)
        print(address," 已上线")
        GateServer.clients[key] = stream
        try:
            while True:
                print("receive ... ")
                msg = yield stream.read_bytes( 1024, partial = True )
                print msg, 'from', address
                if msg == 'over':
                    stream.close()
                    if key in GateServer.clients:
                        del GateServer.clients[key]
                else:
                    GateServer.receive_q.put((1,msg))
                    # self.logic.input(msg)
                    # result = self.logic.input(msg)
                    # if result is not None:
                    #     yield stream.write(result)
        except iostream.StreamClosedError as e:
            print("error",e)
            stream.close()
            if key in GateServer.clients:
                del GateServer.clients[key]