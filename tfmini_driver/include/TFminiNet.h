#include <ros/ros.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <termios.h>
#include <errno.h>
#include <string>
#include <sensor_msgs/Range.h>
#include <deque>
#include <mutex>
#include <epoll_client.hpp>
using namespace std;
using namespace transport;

namespace benewake
{
  class TFminiNet
  {
    public:
      TFminiNet(const ros::NodeHandle &nh = ros::NodeHandle("~"));
      ~TFminiNet(){};
      float getDist();
      void closePort();
      void update();

    private:
      ros::NodeHandle nh_;
      ros::Publisher pub_range;
      sensor_msgs::Range TFmini_range;
      std::string device_ip;
      int device_port;
      float dist = 0;

      std::mutex que_mtx;
      std::shared_ptr<EpollTcpClient> tcp_ptr;
      std::deque<std::vector<unsigned char>> receive_msg;
      vector<unsigned char> queue_pop(){
        if(!receive_msg.empty() && que_mtx.try_lock()){
            auto msg = receive_msg.front();
            for (size_t i = 0; i < receive_msg.size(); i++)
            {
              receive_msg.pop_front();
            }
            que_mtx.unlock();
            return msg;
        }
        return {};
      }
      bool readData(unsigned char *_buf, int _nRead);
  };
}
