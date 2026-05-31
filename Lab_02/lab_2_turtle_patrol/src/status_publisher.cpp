#include <chrono>
#include <functional>
#include <memory>
#include <string>
// #include <cmath>
#include "rclcpp/rclcpp.hpp"
#include "turtlesim/msg/pose.hpp"

#include "lab_2_turtle_patrol/msg/robot_status.hpp"

using namespace std::chrono_literals;
using std::placeholders::_1;

class PatrolPub : public rclcpp::Node {
public:
  PatrolPub() : Node("patrol_status_pub") {

    // make a parameter for the rate
    this->declare_parameter("status_rate", 5.0);

    this->get_parameter("status_rate", status_rate_);

    subscription_ = this->create_subscription<turtlesim::msg::Pose>(
        "turtle1/pose", 10, std::bind(&PatrolPub::pose_callback, this, _1));

    publisher_ = this->create_publisher<lab_2_turtle_patrol::msg::RobotStatus>(
        "robot/status", 10);
    timer_ = this->create_wall_timer(
        1000ms / status_rate_, std::bind(&PatrolPub::timer_callback, this));
  }

private:
  void timer_callback() {
    auto msg = lab_2_turtle_patrol::msg::RobotStatus();

    // get from trurtlesim::msg::Pose to geometry_msgs::msg::Pose
    msg.pose.x = last_pose_->x;
    msg.pose.y = last_pose_->y;
    msg.pose.theta = last_pose_->theta;

    msg.state = state_;
    msg.temperature = 30.0;
    msg.lap_count = lap_count_;

    publisher_->publish(msg);
  }

  void pose_callback(const turtlesim::msg::Pose::SharedPtr msg) {
    last_pose_ = msg;
    if (abs(msg->linear_velocity) > 0) {
      state_ = "running";
    } else {
      state_ = "stopped";
    }
    bool is_near_center =
        std::abs(msg->x - 5.54444) < 0.05 && std::abs(msg->y - 5.54444) < 0.05;

    // detect rising edge (outside -> inside)
    if (state_ == "running" && is_near_center && !near_center_) {
      lap_count_++;
      RCLCPP_INFO(this->get_logger(), "Lap: %d", lap_count_);
    }

    near_center_ = is_near_center;

    RCLCPP_INFO(this->get_logger(), "I heard: [%f, %f, %f]", msg->x, msg->y,
                msg->theta);
  }
  rclcpp::TimerBase::SharedPtr timer_;
  rclcpp::Publisher<lab_2_turtle_patrol::msg::RobotStatus>::SharedPtr
      publisher_;

  rclcpp::Subscription<turtlesim::msg::Pose>::SharedPtr subscription_;

  turtlesim::msg::Pose::SharedPtr last_pose_;

  int32_t lap_count_ = 0;
  std::string state_ = "running";

  double status_rate_;
  bool near_center_ = false;
};

int main(int argc, char *argv[]) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<PatrolPub>());
  rclcpp::shutdown();
  return 0;
}