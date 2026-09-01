from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('mission_changeset_path', default_value='/tmp/changeset.json'),
        DeclareLaunchArgument('executor_id', default_value='apex-ros2-executor'),
        DeclareLaunchArgument('log_level', default_value='info'),
        
        Node(
            package='apex_autonomy',
            executable='mission_contract_executor',
            name='mission_contract_executor',
            parameters=[{
                'mission_changeset_path': LaunchConfiguration('mission_changeset_path'),
                'executor_id': LaunchConfiguration('executor_id')
            }],
            ros_arguments=['--log-level', LaunchConfiguration('log_level')]
        ),
        
        Node(
            package='apex_autonomy',
            executable='telemetry_bridge',
            name='telemetry_bridge',
            ros_arguments=['--log-level', LaunchConfiguration('log_level')]
        ),
        
        Node(
            package='apex_autonomy',
            executable='orbital_trajectory_node',
            name='orbital_trajectory_node',
            ros_arguments=['--log-level', LaunchConfiguration('log_level')]
        )
    ])
