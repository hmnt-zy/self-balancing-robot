import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription

from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch.substitutions import (
    LaunchConfiguration,
    PathJoinSubstitution
)

from launch_ros.substitutions import FindPackageShare

from launch_ros.actions import Node


def generate_launch_description():

    # Package locations
    pkg_share = get_package_share_directory('sb_gazebo')
    description_pkg_share = get_package_share_directory('sb_description')
    ros_gz_sim_share = get_package_share_directory('ros_gz_sim')


    # Launch files
    rsp_launch_path = os.path.join(
        description_pkg_share,
        'launch',
        'rsp.launch.py'
    )

    gz_sim_launch = os.path.join(
        ros_gz_sim_share,
        'launch',
        'gz_sim.launch.py'
    )


    # Arguments
    use_sim_time = LaunchConfiguration(
        'use_sim_time'
    )

    world_file = LaunchConfiguration(
        'world'
    )


    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation time'
    )


    # Default world inside package
    default_world = PathJoinSubstitution([
        FindPackageShare('sb_gazebo'),
        'worlds',
        'empty_world.sdf'
    ])


    declare_world = DeclareLaunchArgument(
        'world',
        default_value=default_world,
        description='Gazebo world file'
    )


    gz_args = [
        '-r ',
        world_file
    ]


    include_rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            rsp_launch_path
        ),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'run_jsp': 'false'
        }.items()
    )


    include_gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            gz_sim_launch
        ),
        launch_arguments={
            'gz_args': gz_args
        }.items()
    )


    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        name='urdf_spawner',
        output='screen',
        arguments=[
            '-topic',
            'robot_description',
            '-name',
            'my_robot',
            '-x',
            '0.0',
            '-y',
            '0.0',
            '-z',
            '0.1'
        ]
    )


    bridge = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                pkg_share,
                'launch',
                'sim_bridge.launch.py'
            )
        )
    )


    return LaunchDescription([
        declare_use_sim_time,
        declare_world,
        include_rsp,
        include_gz_sim,
        spawn_robot,
        bridge
    ])