#include <chrono>
#include <functional>
#include <memory>

#include <fstream>

#include "rclcpp/rclcpp.hpp"
#include "nav_msgs/msg/odometry.hpp"

using namespace std::chrono_literals;

class OdomSimulator : public rclcpp::Node {
public:
  OdomSimulator() : Node("odom_simulator") {

    publisher_ = this->create_publisher<nav_msgs::msg::Odometry>("odom", 10);
    timer_ = this->create_wall_timer(
        500ms, std::bind(&OdomSimulator::timer_callback, this));
  }

private:
  void timer_callback() {
    auto message = nav_msgs::msg::Odometry();
    message.header.stamp = this->get_clock()->now();
    message.header.frame_id = "odom";
    message.child_frame_id = "base_link";
    message.pose.pose.position.x = odom_pose_x;
    message.pose.pose.position.y = 0;
    message.pose.pose.position.z = 0;
    message.pose.pose.orientation.x = 0;
    message.pose.pose.orientation.y = 0;
    message.pose.pose.orientation.z = 0;
    message.pose.pose.orientation.w = 1;

    // speed equals distance (0.1) / time (0.5)
    message.twist.twist.linear.x = 0.2;
    message.twist.twist.linear.y = 0;
    message.twist.twist.linear.z = 0;
    message.twist.twist.angular.x = 0;
    message.twist.twist.angular.y = 0;
    message.twist.twist.angular.z = 0;


    RCLCPP_INFO(this->get_logger(), "Publishing: '%f'", message.pose.pose.position.x);
    publisher_->publish(message);
    odom_pose_x += 0.1;
  }
  rclcpp::TimerBase::SharedPtr timer_;
  rclcpp::Publisher<nav_msgs::msg::Odometry>::SharedPtr publisher_;
  float_t odom_pose_x = 0;
};

int main(int argc, char *argv[]) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<OdomSimulator>());
  rclcpp::shutdown();
  return 0;
}