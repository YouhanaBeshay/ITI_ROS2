from ament_index_python.packages import get_package_share_directory
import os



from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    """Generate launch description with static transform publishers."""
    
    config_path = os.path.join(
    get_package_share_directory('lab_3_pkg_tf'),
        'config',
        'ekf.yaml'
    )
    rviz_path = os.path.join(
        get_package_share_directory('lab_3_pkg_tf'),
        'config',
        'robot_tf.rviz'
    )

    return LaunchDescription([
        
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=[
                '--x', '0.0',      
                '--y', '0.0',
                '--z', '0.05',
                '--roll', '0.0',   
                '--pitch', '0.0',
                '--yaw', '0.0',
                '--frame-id', 'base_footprint',
                '--child-frame-id', 'base_link'
            ],
            name='base_footprint_to_base_link_broadcaster'
        ),

        
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=[
                '--x', '0.5',
                '--y', '-0.1',
                '--z', '0.0',
                '--roll', '0.0',
                '--pitch', '0.0',
                '--yaw', '0.0',
                '--frame-id', 'base_link',
                '--child-frame-id', 'imu_link'
            ],
            name='base_link_to_imu_link_broadcaster'
        ),

        
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=[
                '--x', '0.2',      
                '--y', '0.0',     
                '--z', '0.25',      
                '--roll', '0.0',
                '--pitch', '0.0', 
                '--yaw', '0.0',
                '--frame-id', 'base_link',
                '--child-frame-id', 'gps_link'
            ],
            name='base_link_to_gps_link_broadcaster'
        ),


        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=[
                '--x', '0.5',      
                '--y', '0.15',      
                '--z', '0.1',     
                '--roll', '0.0',
                '--pitch', '0.0',
                '--yaw', '0.785',
                '--frame-id', 'base_link',
                '--child-frame-id', 'ultrasonic1_link'
            ],
            name='base_link_to_ultrasonic1_link_broadcaster'
        ),
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=[
                '--x', '0.5',      
                '--y', '0.0',      
                '--z', '0.1',    
                '--roll', '0.0',
                '--pitch', '0.0',
                '--yaw', '0.0',
                '--frame-id', 'base_link',
                '--child-frame-id', 'ultrasonic2_link'
            ],
            name='base_link_to_ultrasonic2_link_broadcaster'
        ),

        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=[
                '--x', '0.5',      
                '--y', '-0.15',      
                '--z', '0.1',     
                '--roll', '0.0',
                '--pitch', '0.0',
                '--yaw', '-0.785',
                '--frame-id', 'base_link',
                '--child-frame-id', 'ultrasonic3_link'
            ],
            name='base_link_to_ultrasonic3_link_broadcaster'
        ),

        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=[
                '--x', '-0.1',      
                '--y', '0.15',     
                '--z', '0.1',     
                '--roll', '0.0',
                '--pitch', '0.0',
                '--yaw', '2.357142857',
                '--frame-id', 'base_link',
                '--child-frame-id', 'ultrasonic4_link'
            ],
            name='base_link_to_ultrasonic4_link_broadcaster'
        ),
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=[
                '--x', '-0.1',      
                '--y', '0',      
                '--z', '0.1',     
                '--roll', '0.0',
                '--pitch', '0.0',
                '--yaw', '3.14',
                '--frame-id', 'base_link',
                '--child-frame-id', 'ultrasonic5_link'
            ],
            name='base_link_to_ultrasonic5_link_broadcaster'
        ),
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=[
                '--x', '-0.1',      
                '--y', '-0.15',      
                '--z', '0.1',     
                '--roll', '0.0',
                '--pitch', '0.0',
                '--yaw', '-2.357142857',
                '--frame-id', 'base_link',
                '--child-frame-id', 'ultrasonic6_link'
            ],
            name='base_link_to_ultrasonic6_link_broadcaster'
        ),
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node',
            output='screen',
            parameters=[config_path],
            remappings=[
                ('odometry/filtered', '/odometry/local')
            ]
        ),
        
        Node(
            package='lab_3_pkg_tf',
            executable='orientation_analysis.py',
            name='orientation_analysis',
            output='screen'
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', rviz_path]
        )
    ])