from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    bridge = Node(
    package="ros_gz_bridge",
    executable="parameter_bridge",
    arguments=[
        "/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock",
        "/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist",
        "/imu@sensor_msgs/msg/Imu[gz.msgs.IMU",
        "/joint_states@sensor_msgs/msg/JointState[gz.msgs.Model",
    ],
    output="screen",
)

    return LaunchDescription([
        bridge,
    ])