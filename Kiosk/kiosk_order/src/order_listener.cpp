#include <ros/ros.h>
#include <std_msgs/String.h>

void orderCallback(const std_msgs::String::ConstPtr& msg)
{
    ROS_INFO("주문 수신: %s", msg->data.c_str());
}

int main(int argc, char **argv)
{
    ros::init(argc, argv, "order_listener");
    ros::NodeHandle n;

    ros::Subscriber sub = n.subscribe("/order_topic", 1000, orderCallback);

    ros::spin();
    return 0;
}
