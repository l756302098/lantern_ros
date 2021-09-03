#!/usr/bin/env python
#coding=utf-8
from tornado import ioloop, gen, iostream
from tornado.tcpserver import TCPServer

class GateServer( TCPServer ):
    @gen.coroutine
    def handle_stream( self, stream, address ):
        try:
            print("get client ",address)
            while True:
                print("receive ... ")
                msg = yield stream.read_bytes( 1024, partial = True )
                print msg, 'from', address
                if msg == 'over':
                    stream.close()
                else:
                    result = self.logic.input(msg)
                    if result is not None:
                        yield stream.write(result)
        except iostream.StreamClosedError as e:
            stream.close()
            print("error",e)