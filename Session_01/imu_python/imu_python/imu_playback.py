import rclpy
from rclpy.node import Node
import random

from sensor_msgs.msg import Imu
import os
import csv
class ImuPlayback(Node):
    def __init__(self):
        super().__init__('Imu_pub')
        self.publisher_ = self.create_publisher(Imu, 'imu/data', 10)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        # absolute path of csv
        self.csv_path = "/home/youhana/Downloads/imu_data.csv"
        
        # Load CSV once
        self.rows = []

        with open(self.csv_path, mode='r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                self.rows.append(row)
                

        # Current playback index
        self.current_index = 0  
              
    def timer_callback(self):

        row = self.rows[self.current_index]
        msg = Imu()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'
        # Orientation
        msg.orientation.w = float(row['orient_w'])
        msg.orientation.x = float(row['orient_x'])
        msg.orientation.y = float(row['orient_y'])
        msg.orientation.z = float(row['orient_z'])
        # Angular velocity
        msg.angular_velocity.x = float(row['ang_x'])
        msg.angular_velocity.y = float(row['ang_y'])
        msg.angular_velocity.z = float(row['ang_z'])
        # Linear acceleration
        msg.linear_acceleration.x = float(row['acc_x'])
        msg.linear_acceleration.y = float(row['acc_y'])
        msg.linear_acceleration.z = float(row['acc_z'])
        self.publisher_.publish(msg)
        self.get_logger().info(
            f'Published row {self.current_index}'
        )
        # Move to next row
        self.current_index += 1
        # Loop back after last row
        self.current_index %= len(self.rows)
        
def main(args=None):
    rclpy.init(args=args)

    Imu_pub = ImuPlayback()

    rclpy.spin(Imu_pub)

    Imu_pub.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
