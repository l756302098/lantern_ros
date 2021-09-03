#include <TFminiNet.h>
#include "ros/ros.h"

int main(int argc, char **argv)
{
  ros::init(argc, argv, "tfmini_net_node");
  benewake::TFminiNet tn;

  ROS_INFO_STREAM("Start processing ...");
  ros::Rate loop_rate(30);
  while(ros::master::check() && ros::ok())
  {
    tn.update();
    ros::spinOnce();
    loop_rate.sleep();
  }

  tn.closePort();
}