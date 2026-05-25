#include <chrono>
#include <functional>
#include <memory>


#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"

using std::placeholders::_1;

class VelocityLimiter : public rclcpp::Node {
public:
  VelocityLimiter() : Node("velocity_limiter") {

    publisher_ = this->create_publisher<geometry_msgs::msg::Twist>("cmd_vel_limited", 10);
    subscription_ = this->create_subscription<geometry_msgs::msg::Twist>(
        "cmd_vel", 10, std::bind(&VelocityLimiter::topic_callback, this, _1));

  }

  void topic_callback(const geometry_msgs::msg::Twist & msg) const {
    // if any linear velocity exceeds 1 m/s, limit it to 1 m/s
    geometry_msgs::msg::Twist msg_limited = msg;

    if (msg.linear.x > 1.0 || msg.linear.x < -1.0)
    {
        msg_limited.linear.x = 1.0;
    }
    if(msg.angular.z > 1.5 || msg.angular.z < -1.5)
    {
        msg_limited.angular.z = 1.0;
    }
    
    publisher_->publish(msg_limited);
  }

private:
 
  rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_;
  rclcpp::Subscription<geometry_msgs::msg::Twist>::SharedPtr subscription_;
};

int main(int argc, char *argv[]) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<VelocityLimiter>());
  rclcpp::shutdown();
  return 0;
}