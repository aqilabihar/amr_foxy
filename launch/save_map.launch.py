import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    package_name = 'suraqil_bot' 
    pkg_dir = get_package_share_directory(package_name)
    config_file = os.path.join(pkg_dir, 'config', 'map_saver.yaml')
    
    # KUNCI PERBAIKAN: Tembak langsung ke folder src/amr_foxy/maps
    # (Menggunakan os.path.expanduser('~') agar otomatis mendeteksi /home/suraqil)
    map_save_path = os.path.join(os.path.expanduser('~'), 'amr_ws', 'src', 'amr_foxy', 'maps', 'peta_pertama')

    save_map_cmd = ExecuteProcess(
        cmd=['ros2', 'run', 'nav2_map_server', 'map_saver_cli', 
             '-f', map_save_path, 
             '--ros-args', '--params-file', config_file],
        output='screen'
    )

    return LaunchDescription([
        save_map_cmd
    ])