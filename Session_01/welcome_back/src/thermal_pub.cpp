#include <chrono>
#include <functional>
#include <memory>

#include <fstream>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/float32.hpp"

using namespace std::chrono_literals;

class ThermalPub : public rclcpp::Node {
public:
  ThermalPub() : Node("thermal_pub") {

    publisher_ = this->create_publisher<std_msgs::msg::Float32>("cpu_temp", 10);
    timer_ = this->create_wall_timer(
        500ms, std::bind(&ThermalPub::timer_callback, this));
  }

private:
  void timer_callback() {

    auto message = std_msgs::msg::Float32();
    // get data from file /sys/class/thermal/thermal_zone0/temp
    std::fstream file;
    file.open("/sys/class/thermal/thermal_zone2/temp", std::ios::in);
    file >> message.data;
    file.close();
    RCLCPP_INFO(this->get_logger(), "Cpu Temp: '%f' C", message.data/1000);
    publisher_->publish(message);
  }
  rclcpp::TimerBase::SharedPtr timer_;
  rclcpp::Publisher<std_msgs::msg::Float32>::SharedPtr publisher_;
};

int main(int argc, char *argv[]) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<ThermalPub>());
  rclcpp::shutdown();
  return 0;
}