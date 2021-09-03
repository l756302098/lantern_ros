#include <TFminiNet.h>

namespace benewake
{
    TFminiNet::TFminiNet(const ros::NodeHandle &nh):nh_(nh){
        nh_.param<std::string>("device_ip", device_ip, "192.168.1.4");
        nh_.param<int>("device_port", device_port, 1001);
        std::cout << "ip:" << device_ip << " port:" << device_port << std::endl;
        pub_range = nh_.advertise<sensor_msgs::Range>("/TFmini", 1, true);
        TFmini_range.radiation_type = sensor_msgs::Range::INFRARED;
        TFmini_range.field_of_view = 0.04;
        TFmini_range.min_range = 0.3;
        TFmini_range.max_range = 12;
        TFmini_range.header.frame_id = "/TFmini";
        float dist = 0;
        tcp_ptr = std::make_shared<EpollTcpClient>(device_ip, device_port);
        if (!tcp_ptr) {
            std::cout << "tcp_client create faield!" << std::endl;
            ros::shutdown();
        }
        auto recv_call = [&](const PacketPtr& data) -> void {
            // just print recv data to stdout
            std::vector<unsigned char> rv;
            char *p=(char*)data->msg.c_str();
            int sum = 0;
            for(int i = 0; i < sizeof(p); i++){
                sum += p[i];
            }
            sum = sum % 256;
            rv.insert(rv.end(),p,p+data->msg.size());
            que_mtx.lock();
            receive_msg.push_back(rv);
            que_mtx.unlock();
            return;
        };
        tcp_ptr->RegisterOnRecvCallback(recv_call);
        if (!tcp_ptr->Start()) {
            std::cout << "tcp_client start failed!" << std::endl;
            ros::shutdown();
        }
        std::cout << "############tcp_client started!################" << std::endl;
    }

    float TFminiNet::getDist(){
        vector<unsigned char> data = queue_pop();
        if(data.size() != 9) return -1; 
        if(data[0] == 0x59 && data[1] == 0x59){
            int sumCheck = 0;
            for(int i = 0; i < 8; i++)
            {
                sumCheck += data[i];
                //printf(" %x ",data[i]);
            }
            sumCheck = sumCheck % 256;
            //printf("%x %x \n",sumCheck,dataBuf[8]);
            if(sumCheck == data[8])
            {
                return ((float)(data[3] << 8 | data[2]) / 100.0);
            }
            else
            {
                return 0.0;
            }
        }
        return -1;
    }
    void TFminiNet::closePort(){
        if(tcp_ptr)
            tcp_ptr->Stop();
    }

    void TFminiNet::update(){
        dist = getDist();
        if(dist > 0 && dist < TFmini_range.max_range)
        {
            TFmini_range.range = dist;
            TFmini_range.header.stamp = ros::Time::now();
            pub_range.publish(TFmini_range);
        }
        // else if(dist == -1.0)
        // {
        //     ROS_ERROR_STREAM("Failed to read data. TFmini ros node stopped!");
        // }      
        // else if(dist == 0.0)
        // {
        //     ROS_ERROR_STREAM("Data validation error!");
        // }
    }

    bool TFminiNet::readData(unsigned char *_buf, int _nRead){

    }
}