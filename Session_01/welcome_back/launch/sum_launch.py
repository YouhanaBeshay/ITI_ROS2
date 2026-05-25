import launch
import launch_ros.actions


def generate_launch_description():

    pub_b = launch_ros.actions.Node(
        package='welcome_back',
        executable='pub_a',
        name='Publisher_B',

        # topic remap
        remappings=[
            ('topic_a', 'topic_b')
        ]
    )

    pub_a = launch_ros.actions.Node(
        package='welcome_back',
        executable='pub_a',

        # parameters
        parameters=[
            {
                'max_value': 500,
                'min_value': 100
            }
        ]
    )

    sum_sub = launch_ros.actions.Node(
        package='welcome_back',
        executable='sum_sub'
    )

    return launch.LaunchDescription([
        pub_b,
        pub_a,
        sum_sub
    ])