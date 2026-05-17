import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Pastikan nama paket sesuai dengan di CMakeLists.txt (suraqil_bot atau amr_foxy)
    package_name = 'suraqil_bot' 
    
    # Jalur langsung ke file peta di folder src agar aman dari colcon clean
    map_file_path = os.path.join(os.path.expanduser('~'), 'amr_ws', 'src', 'amr_foxy', 'maps', 'peta_pertama.yaml')

    # 1. Node Map Server (Pemuat Gambar Peta)
    map_server_node = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        output='screen',
        parameters=[{'use_sim_time': True},
                    {'yaml_filename': map_file_path}]
    )

    # 2. Node Lifecycle Manager (Pembangun Status Map Server)
    lifecycle_manager_node = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_map',
        output='screen',
        parameters=[{'use_sim_time': True},
                    {'autostart': True},
                    {'node_names': ['map_server']}]
    )

    # 3. Jembatan Koordinat Sementara (Map -> Odom)
    static_tf_node = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['0', '0', '0', '0', '0', '0', 'map', 'odom']
    )

    return LaunchDescription([
        map_server_node,
        lifecycle_manager_node,
        static_tf_node
    ])