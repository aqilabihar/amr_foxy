import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_dir = get_package_share_directory('suraqil_bot')
    map_path = os.path.join(pkg_dir, 'maps', 'peta_pertama.yaml')
    
    # Explicitly point to your updated parameters file
    nav2_params_path = os.path.join(pkg_dir, 'config', 'nav2_params.yaml')
    twist_mux_params = os.path.join(pkg_dir, 'config', 'twist_mux.yaml')

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

    # 3. Localization (Passing your nav2_params.yaml explicitly)
    localization = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(pkg_dir, 'launch', 'localization_launch.py')]),
        launch_arguments={
            'use_sim_time': 'true', 
            'autostart': 'true', 
            'map': map_path,
            'params_file': nav2_params_path
        }.items()
    )
    delay_loc = TimerAction(period=5.0, actions=[localization])

    # 4. Nav2 Navigation Stack (Passing your nav2_params.yaml explicitly)
    navigation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(pkg_dir, 'launch', 'navigation_launch.py')]),
        launch_arguments={
            'use_sim_time': 'true', 
            'autostart': 'true',
            'params_file': nav2_params_path
        }.items()
    )
    delay_nav = TimerAction(period=8.0, actions=[navigation])

    # 5. Twist Mux 
    twist_mux_node = Node(
        package='twist_mux', executable='twist_mux', name='twist_mux', output='screen',
        parameters=[twist_mux_params, {'use_sim_time': True}],
        remappings=[('cmd_vel_out', 'cmd_vel')]
    )

    return LaunchDescription([
        sim,
        rviz,
        delay_loc,
        delay_nav,
        twist_mux_node
    ])