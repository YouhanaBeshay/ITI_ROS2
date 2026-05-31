
import os
from ament_index_python.packages import get_package_share_directory
import launch
import launch_ros.actions


def generate_launch_description():
    
    params_file = os.path.join(
        get_package_share_directory('lab_2_turtle_patrol'),
        'params',
        'patrol_params.yaml'
    )
    
    
    # turtlesim 
    turtlesim_node = launch_ros.actions.Node(
        package='turtlesim',
        executable='turtlesim_node',
        name='turtlesim',
        output='screen'
    )
    
    # node 1 ( status publisher )
    status_publisher_node = launch_ros.actions.Node(
        package='lab_2_turtle_patrol',
        executable='status_publisher',
        name='status_publisher',
        output='screen',
        parameters=[params_file]
    )

    # node 2 ( patrol controller )
    patrol_controller_node = launch_ros.actions.Node(
        package='lab_2_turtle_patrol',
        executable='patrol_controller',
        name='patrol_controller',
        output='screen',
        parameters=[params_file]
    )
    
    

    return launch.LaunchDescription([
        turtlesim_node,
        status_publisher_node,
        patrol_controller_node
    ])