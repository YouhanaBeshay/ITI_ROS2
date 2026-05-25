import rclpy
from rclpy.node import Node
import random

from std_msgs.msg import Float32

class DistPublisher(Node):
    def __init__(self):
        super().__init__('dist_publisher')
        self.publisher_ = self.create_publisher(Float32, 'sensor/distance', 10)
        timer_period = 0.2  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        
    def timer_callback(self):
        msg = Float32()
        msg.data = random.uniform(0.03,5.0)
        self.get_logger().info(f"Published distance: {msg.data}")
        self.publisher_.publish(msg)
        
def main(args=None):
    rclpy.init(args=args)

    dist_publisher = DistPublisher()

    rclpy.spin(dist_publisher)

    dist_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
