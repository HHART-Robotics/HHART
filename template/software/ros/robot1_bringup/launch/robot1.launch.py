import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    share = get_package_share_directory("robot1_bringup")
    with open(os.path.join(share, "urdf", "robot1.urdf"), encoding="utf-8") as f:
        description = f.read()
    controllers = os.path.join(share, "config", "controllers.yaml")
    return LaunchDescription([
        Node(package="robot_state_publisher", executable="robot_state_publisher",
             parameters=[{"robot_description": description}]),
        Node(package="controller_manager", executable="ros2_control_node", parameters=[controllers],
             remappings=[("~/robot_description", "/robot_description")]),
        Node(package="controller_manager", executable="spawner", arguments=["joint_state_broadcaster"]),
        Node(package="controller_manager", executable="spawner", arguments=["diff_drive_controller"]),
        # Drivers from robot1.repos go here, e.g. Node(package="lidar_driver", executable="lidar_node")
        Node(package="robot1", executable="robot1-robot", arguments=["--controller", "diff_drive_controller"],
             output="screen"),
    ])
