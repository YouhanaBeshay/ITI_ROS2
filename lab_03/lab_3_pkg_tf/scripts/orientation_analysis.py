#!/usr/bin/env python3
"""
Orientation Analysis Node 
Subscribes to:
  - /imu/data (sensor_msgs/Imu) with qos_profile_sensor_data
  - /odometry/local (nav_msgs/Odometry) with qos_profile_sensor_data
Periodically logs and compares the yaw orientation from each source.
"""

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Imu
from nav_msgs.msg import Odometry
import math


class OrientationAnalysisNode(Node):
    def __init__(self):
        super().__init__('orientation_analysis')

        # Subscribers
        self.imu_sub = self.create_subscription(
            Imu,
            '/imu/data/bag',
            self.imu_callback,
            qos_profile_sensor_data
        )

        self.odom_sub = self.create_subscription(
            Odometry,
            '/odometry/local',
            self.odom_callback,
            qos_profile_sensor_data
        )

        self.latest_imu_yaw = None
        self.latest_odom_yaw = None
        self.last_imu_time = None
        self.last_odom_time = None

        # logging (every 1 second)
        self.timer = self.create_timer(1.0, self.compare_and_log)

        self.get_logger().info('Orientation Analysis Node started.')

    def quaternion_to_rpy(self, x, y, z, w):
        """
        Convert quaternion [x, y, z, w] to roll-pitch-yaw (in radians).
        """
        # Normalize first
        norm = math.sqrt(x*x + y*y + z*z + w*w)
        if norm == 0.0:
            return [0.0, 0.0, 0.0]
        x /= norm
        y /= norm
        z /= norm
        w /= norm

        # Roll (x-axis rotation)
        sinr_cosp = 2.0 * (w * x + y * z)
        cosr_cosp = 1.0 - 2.0 * (x * x + y * y)
        roll = math.atan2(sinr_cosp, cosr_cosp)

        # Pitch (y-axis rotation)
        sinp = 2.0 * (w * y - z * x)
        if abs(sinp) >= 1.0:
            pitch = math.copysign(math.pi / 2.0, sinp)
        else:
            pitch = math.asin(sinp)

        # Yaw (z-axis rotation)
        siny_cosp = 2.0 * (w * z + x * y)
        cosy_cosp = 1.0 - 2.0 * (y * y + z * z)
        yaw = math.atan2(siny_cosp, cosy_cosp)

        return [roll, pitch, yaw]

    def imu_callback(self, msg: Imu):
        """Extract yaw from IMU quaternion."""
        q = msg.orientation
        _, _, yaw = self.quaternion_to_rpy(q.x, q.y, q.z, q.w)
        self.latest_imu_yaw = yaw
        self.last_imu_time = msg.header.stamp

    def odom_callback(self, msg: Odometry):
        """Extract yaw from Odometry quaternion."""
        q = msg.pose.pose.orientation
        _, _, yaw = self.quaternion_to_rpy(q.x, q.y, q.z, q.w)
        self.latest_odom_yaw = yaw
        self.last_odom_time = msg.header.stamp

    def normalize_angle(self, angle):
        """Normalize angle to [-pi, pi]."""
        while angle > math.pi:
            angle -= 2.0 * math.pi
        while angle < -math.pi:
            angle += 2.0 * math.pi
        return angle

    def compare_and_log(self):
        """Periodically log and compare yaw from both sources."""
        if self.latest_imu_yaw is None:
            self.get_logger().warn('No IMU data received yet.')
            return
        if self.latest_odom_yaw is None:
            self.get_logger().warn('No Odometry data received yet.')
            return

        imu_yaw_deg = math.degrees(self.latest_imu_yaw)
        odom_yaw_deg = math.degrees(self.latest_odom_yaw)
        diff = self.normalize_angle(self.latest_imu_yaw - self.latest_odom_yaw)
        diff_deg = math.degrees(diff)

        self.get_logger().info(
            f'Yaw Comparison — '
            f'IMU: {imu_yaw_deg:8.3f}° | '
            f'Odometry: {odom_yaw_deg:8.3f}° | '
            f'Difference: {diff_deg:8.3f}°'
        )


def main(args=None):
    rclpy.init(args=args)
    node = OrientationAnalysisNode()
    
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()