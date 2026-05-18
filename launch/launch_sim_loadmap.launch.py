import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_dir = get_package_share_directory('suraqil_bot')
    map_path = os.path.join(pkg_dir, 'maps', 'peta_pertama.yaml')

    # 1. Gazebo Sim
    sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(pkg_dir, 'launch', 'launch_sim.launch.py')])
    )

    # 2. RViz2
    rviz = Node(
        package='rviz2', executable='rviz2', name='rviz2', output='screen',
        arguments=['-d', os.path.join(pkg_dir, 'config', 'map.rviz')],
        parameters=[{'use_sim_time': True}]
    )

    # 3. Manual Map Server Node (Bypasses nav2_params.yaml completely)
    map_server_node = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        output='screen',
        parameters=[{
            'yaml_filename': map_path,
            'use_sim_time': True
        }]
    )

    # 4. Manual Lifecycle Manager Node
    lifecycle_manager_node = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_map',
        output='screen',
        parameters=[{
            'use_sim_time': True,
            'autostart': True,
            'node_names': ['map_server']
        }]
    )

    # Group map nodes together with a 5-second delay for Gazebo clock stability
    delay_map_nodes = TimerAction(
        period=5.0,
        actions=[map_server_node, lifecycle_manager_node]
    )

    # 5. Fake TF Link (Connect map -> odom)
    fake_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['0', '0', '0', '0', '0', '0', 'map', 'odom'],
        parameters=[{'use_sim_time': True}]
    )

    return LaunchDescription([
        sim,
        rviz,
        delay_map_nodes,
        fake_tf
    ])