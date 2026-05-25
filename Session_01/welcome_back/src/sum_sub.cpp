#include <limits>
#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/int32.hpp"
using std::placeholders::_1;
using namespace std::chrono_literals;


class SumSubscriber : public rclcpp::Node {
public:
  SumSubscriber() : Node("sum_subscriber") {
    subscription_A = this->create_subscription<std_msgs::msg::Int32>(
        "topic_a", 10, std::bind(&SumSubscriber::topic_A_callback, this, _1));

    subscription_B = this->create_subscription<std_msgs::msg::Int32>(
        "topic_b", 10, std::bind(&SumSubscriber::topic_B_callback, this, _1));


    publisher_ = this->create_publisher<std_msgs::msg::Int32>("topic_sum", 10);

  }

private:
  void topic_A_callback(const std_msgs::msg::Int32 &msg)  {
    input_A = msg.data;
    check_sum();
    
  }
  void topic_B_callback(const std_msgs::msg::Int32 &msg)  {
    input_B = msg.data;
    check_sum();
    
  }
  void check_sum()  {

    if (input_A != std::numeric_limits<int32_t>::min() && input_B != std::numeric_limits<int32_t>::min()) {
        
      sum = input_A + input_B;
      auto message = std_msgs::msg::Int32();
      message.data = sum;
      RCLCPP_INFO(this->get_logger(), "Publishing Sum: '%d'", message.data);
      publisher_->publish(message);
    }
      
  }

  rclcpp::Subscription<std_msgs::msg::Int32>::SharedPtr subscription_A;
  rclcpp::Subscription<std_msgs::msg::Int32>::SharedPtr subscription_B;

  rclcpp::Publisher<std_msgs::msg::Int32>::SharedPtr publisher_;

  int32_t input_A = std::numeric_limits<int32_t>::min();
  int32_t input_B = std::numeric_limits<int32_t>::min();

  int64_t sum = 0;
};

int main(int argc, char *argv[]) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<SumSubscriber>());
  rclcpp::shutdown();
  return 0;
}