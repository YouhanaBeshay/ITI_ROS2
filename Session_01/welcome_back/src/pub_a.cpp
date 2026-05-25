#include <chrono>
#include <functional>
#include <memory>
#include <random>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/int32.hpp"

using namespace std::chrono_literals;



class PubA : public rclcpp::Node
{
  public:
    PubA()
    : Node("Publisher_A")
    , gen(rd())
    {

      this->declare_parameter("min_value", min);
      this->declare_parameter("max_value", max);


      min = this->get_parameter("min_value").as_int();
      max = this->get_parameter("max_value").as_int();

      dis = std::uniform_int_distribution<int>(min, max);

      publisher_ = this->create_publisher<std_msgs::msg::Int32>("topic_a", 10);
      timer_ = this->create_wall_timer(
      500ms, std::bind(&PubA::timer_callback, this));
    }

  private:
    void timer_callback()
    {
      auto message = std_msgs::msg::Int32();
      message.data = dis(gen);
      RCLCPP_INFO(this->get_logger(), "Publishing: '%d'", message.data);
      publisher_->publish(message);
    }
    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Publisher<std_msgs::msg::Int32>::SharedPtr publisher_;

    // random number generator
    std::random_device rd;
    std::mt19937 gen;
    std::uniform_int_distribution<int> dis;

    // random number limits
    int32_t min = 0;
    int32_t max = 100;

};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<PubA>());
  rclcpp::shutdown();
  return 0;
}