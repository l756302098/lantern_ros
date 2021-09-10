#!/usr/bin/env python
#coding=utf-8
import rospy
from rosbridge_library.internal import message_conversion
from abc import ABCMeta
from importlib import import_module
from server import GateServer
import json

def create_bridge(factory, msg_type, topic_from,topic_to):
    """ generate bridge instance using factory callable and arguments. if `factory` or `meg_type` is provided as string,
     this function will convert it to a corresponding object.
    """
    #print(factory,msg_type,topic_from,topic_to)
    if isinstance(factory, str):
        module_name, obj_name = factory.split(":")
        module = import_module(module_name, 'gateway')
        factory = getattr(module, obj_name)
        print(module_name, obj_name, factory)
        print("factory is isinstance ")
    if not issubclass(factory, Bridge):
        raise ValueError("factory should be Bridge subclass")
    if isinstance(msg_type, str):
        msg_name, msg_obj = msg_type.split(":")
        msg_module = import_module(msg_name)
        msg_type = getattr(msg_module, msg_obj)
        print(module_name, obj_name, msg_type)
        print("msg_type is isinstance ")
    if not issubclass(msg_type, rospy.Message):
        raise TypeError(
            "msg_type should be rospy.Message instance or its string"
            "reprensentation")
    return factory(topic_from=topic_from, msg_type=msg_type, frequency=None)

class Bridge(object):
    """ Bridge base class """
    __metaclass__ = ABCMeta

class RosToTcpBridge(Bridge):
    """ Bridge from ROS topic to TCP

    bridge ROS messages on `topic_from` to TCP. expect `msg_type` ROS message type.
    """

    def __init__(self, topic_from, msg_type, frequency):
        print(topic_from,msg_type,type(msg_type))
        self._topic_from = topic_from
        self._last_published = rospy.get_time()
        self._interval = 0 if frequency is None else 1.0 / frequency
        rospy.Subscriber(topic_from, msg_type, self._callback_ros)

    def _callback_ros(self, msg):
        #rospy.logdebug("ROS received from {}".format(self._topic_from))
        now = rospy.get_time()
        if now - self._last_published >= self._interval:
            self._publish(msg)
            self._last_published = now

    def _publish(self, msg):
        #print("send msg ",msg,type(msg))
        payload = message_conversion.extract_values(msg)
        ds = json.dumps(payload)
        GateServer.send_q.put((10,ds))


__all__ = ['create_bridge', 'Bridge', 'RosToTcpBridge']
