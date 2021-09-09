#!/usr/bin/env python
#coding=utf-8
from tornado import ioloop, gen, iostream
from tornado.tcpserver import TCPServer

class GateServer( TCPServer ):
    @gen.coroutine
    def handle_stream( self, stream, address ):
        print("get client ",address)
        ip = address[0]
        port = address[1]
        key = ip+":"+str(port)
        print(ip,port,key)
        try:
            self.logic.clients[key] = stream
            while True:
                print("receive ... ")
                msg = yield stream.read_bytes( 1024, partial = True )
                print msg, 'from', address
                if msg == 'over':
                    stream.close()
                    if key in self.logic.clients:
                        del self.logic.clients[key]
                else:
                    self.logic.input(msg)
                    # result = self.logic.input(msg)
                    # if result is not None:
                    #     yield stream.write(result)
        except iostream.StreamClosedError as e:
            print("error",e)
            stream.close()
            if key in self.logic.clients:
                del self.logic.clients[key]