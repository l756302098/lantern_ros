#!/usr/bin/env python
#coding=utf-8
from tornado import ioloop, gen, iostream
from tornado.tcpserver import TCPServer

class GateServer( TCPServer ):
    @gen.coroutine
    def handle_stream( self, stream, address ):
        try:
            while True:
                msg = yield stream.read_bytes( 1024, partial = True )
                print msg, 'from', address
                stream.write(str(msg))
                yield stream.write( msg[::-1] )
                if msg == 'over':
                    stream.close()
        except iostream.StreamClosedError:
            pass
            
if __name__ == '__main__':
    server = GateServer()
    server.listen(9091)
    server.start()
    ioloop.IOLoop.current().start()
