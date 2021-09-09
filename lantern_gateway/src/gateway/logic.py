#!/usr/bin/env python
#coding=utf-8
from tornado import ioloop, gen, iostream
from tornado.tcpserver import TCPServer

class Logic():

    def __init__(self):
        self.clients = {}

    def input(self,data):
        """
        receive json data
        """
        print("input:",data)
        return None
    
    def resolveJson(self):
        """
        receive json data
        """
        pass