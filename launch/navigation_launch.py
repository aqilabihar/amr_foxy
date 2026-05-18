# File: ~/amr_ws/src/amr_foxy/launch/navigation_launch.py
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from nav2_common.launch import RewrittenYaml

def generate_launch_description():
    pkg_dir = get_package_share_directory('suraqil_bot') # sesuaikan jika nama pkg berbeda

    namespace = LaunchConfiguration('namespace')
    use_sim_time = LaunchConfiguration('use_sim_time')
    autostart = LaunchConfiguration('autostart')
    params_file = LaunchConfiguration('params_file')

    lifecycle_nodes = ['controller_server', 'planner_server', 'recoveries_server', 'bt_navigator']

    # Rewrite parameters to inject use_sim_time
    param_rewrites = {'use_sim_time': use_sim_time}

    configured_params = RewrittenYaml(
        source_file=params_file,
        root_key=namespace,
        param_rewrites=param_rewrites,
        convert_types=True
    )

    return LaunchDescription([
        SetEnvironmentVariable('RCUTILS_LOGGING_BUFFERED_STREAM', '1'),

        DeclareLaunchArgument('namespace', default_value='', description='Top-level namespace'),
        DeclareLaunchArgument('use_sim_time', default_value='true', description='Use simulation clock if true'),
        DeclareLaunchArgument('autostart', default_value='true', description='Automatically startup the nav2 stack'),
        DeclareLaunchArgument('params_file', default_value=os.path.join(pkg_dir, 'config', 'nav2_params.yaml'), description='Full path to params file'),

        Node(
            package='nav2_controller', executable='controller_server', name='controller_server',
            output='screen', parameters=[configured_params]
        ),
        Node(
            package='nav2_planner', executable='planner_server', name='planner_server',
            output='screen', parameters=[configured_params]
        ),
        Node(
            package='nav2_recoveries', executable='recoveries_server', name='recoveries_server',
            output='screen', parameters=[configured_params]
        ),
        Node(
            package='nav2_bt_navigator', executable='bt_navigator', name='bt_navigator',
            output='screen', parameters=[configured_params]
        ),
        Node(
            package='nav2_lifecycle_manager', executable='lifecycle_manager', name='lifecycle_manager_navigation',
            output='screen', parameters=[{'use_sim_time': use_sim_time, 'autostart': autostart, 'node_names': lifecycle_nodes}]
        )
    ])