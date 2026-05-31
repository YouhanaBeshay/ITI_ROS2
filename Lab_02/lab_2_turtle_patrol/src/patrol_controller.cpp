#include <chrono>
#include <functional>
#include <memory>

#include "geometry_msgs/msg/twist.hpp"
#include "rclcpp/rclcpp.hpp"
#include "std_srvs/srv/empty.hpp"

using namespace std::chrono_literals;

class PatrolController : public rclcpp::Node {
public:
  PatrolController() : Node("patrol_status_pub") {

    // make a parameter for the rate
    this->declare_parameter("linear_speed", 1.5);
    this->declare_parameter("angular_speed", 1.0);

    this->get_parameter("linear_speed", linear_speed_);
    this->get_parameter("angular_speed", angular_speed_);

    publisher_ = this->create_publisher<geometry_msgs::msg::Twist>(
        "turtle1/cmd_vel", 10);
    timer_ = this->create_wall_timer(
        100ms, std::bind(&PatrolController::timer_callback, this));

    // servcies

    stop_service_ = this->create_service<std_srvs::srv::Empty>(
        "stop", std::bind(&PatrolController::stop_callback, this,
                          std::placeholders::_1, std::placeholders::_2));

    continue_service_ = this->create_service<std_srvs::srv::Empty>(
        "continue", std::bind(&PatrolController::continue_callback, this,
                              std::placeholders::_1, std::placeholders::_2));
  }

private:
  void timer_callback() {

    auto msg = geometry_msgs::msg::Twist();

    this->get_parameter("linear_speed", linear_speed_);
    this->get_parameter("angular_speed", angular_speed_);

    if (move_cmd_) {
      msg.linear.x = linear_speed_;
      msg.angular.z = angular_speed_;
    } else {
      msg.linear.x = 0.0;
      msg.angular.z = 0.0;
    }

    publisher_->publish(msg);
  }

  void stop_callback(
      const std::shared_ptr<std_srvs::srv::Empty::Request> request,
      const std::shared_ptr<std_srvs::srv::Empty::Response> response) {
    move_cmd_ = false;
    RCLCPP_INFO(this->get_logger(), "stopped the patrol");
  }

  void continue_callback(
      const std::shared_ptr<std_srvs::srv::Empty::Request> request,
      const std::shared_ptr<std_srvs::srv::Empty::Response> response) {
    move_cmd_ = true;
    RCLCPP_INFO(this->get_logger(), "continuing the patrol");
  }

  rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_;

  rclcpp::Service<std_srvs::srv::Empty>::SharedPtr stop_service_;
  rclcpp::Service<std_srvs::srv::Empty>::SharedPtr continue_service_;

  rclcpp::TimerBase::SharedPtr timer_;
  bool move_cmd_ = true;
  double linear_speed_;
  double angular_speed_;
};

int main(int argc, char *argv[]) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<PatrolController>());
  rclcpp::shutdown();
  return 0;
}