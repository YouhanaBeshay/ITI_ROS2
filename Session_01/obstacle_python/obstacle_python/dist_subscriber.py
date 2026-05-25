import rclpy
from rclpy.node import Node

from std_msgs.msg import Float32
from std_msgs.msg import Bool

class DistSubscriber(Node):
    def __init__(self):
        super().__init__('dist_subscriber')
        self.subscription = self.create_subscription(Float32, 'sensor/distance',self.listener_callback, 10)
        self.subscription
        self.publisher_ = self.create_publisher(Bool, 'cmd/stop', 10)
        
    def listener_callback(self, msg):
        msg_stop = Bool()
        if(msg.data < 2.0):
            self.get_logger().info(f"Detected obstacle!!")
            msg_stop.data = True
        else:
            msg_stop.data = False
    
        self.publisher_.publish(msg_stop)
        
            
        
        
def main(args=None):
    rclpy.init(args=args)

    dist_subscriber = DistSubscriber()

    rclpy.spin(dist_subscriber)

    dist_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
