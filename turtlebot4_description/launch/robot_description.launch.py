# Copyright 2021 Clearpath Robotics, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# @author Roni Kreinin (rkreinin@clearpathrobotics.com)


from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, PathJoinSubstitution
from launch.substitutions.launch_configuration import LaunchConfiguration

from launch_ros.actions import Node


ARGUMENTS = [
    DeclareLaunchArgument('model', default_value='standard',
                          choices=['standard', 'lite'],
                          description='Turtlebot4 Model'),
    DeclareLaunchArgument('use_sim_time', default_value='false',
                          choices=['true', 'false'],
                          description='use_sim_time'),
    DeclareLaunchArgument('namespace', default_value='',
                          description='robot namespace'), 
]


def generate_launch_description():
    pkg_turtlebot4_description = get_package_share_directory('turtlebot4_description')
    xacro_file = PathJoinSubstitution([pkg_turtlebot4_description,
                                       'urdf',
                                       LaunchConfiguration('model'),
                                       'turtlebot4.urdf.xacro'])
    namespace = LaunchConfiguration('namespace')
    frame_prefix = [namespace, '/']

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        namespace=namespace,
        output='screen',
        parameters=[
            {'use_sim_time': LaunchConfiguration('use_sim_time')},
            {'robot_description': Command(['xacro', ' ', xacro_file, ' ',
                                           'gazebo:=ignition ',
                                           'namespace:=', namespace, ' '])},
            {'frame_prefix': frame_prefix},
        ],
    )

    # Define LaunchDescription variable
    ld = LaunchDescription(ARGUMENTS)
    # Add nodes to LaunchDescription
    ld.add_action(robot_state_publisher)
    return ld
