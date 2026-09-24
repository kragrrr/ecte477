"""
    my_node.py

    A ROS node that repeats the map and odometry topic to the correct ecte477 
    namespace topics for map and path.

    Subscribed: /map, /odom, /stack_points
    Publishes: /ecte477/slam_map, /ecte477/explorer, /ecte477/home, /start_explore, /goal_pose
    Created: 2021/04/08
    Author: Brendan Halloran
    Updated 14/04/2026 for ROS2 by Umar Arshad
"""

import rclpy
from rclpy.node import Node
from rclpy.clock import Clock, ClockType
from nav_msgs.msg import OccupancyGrid, Odometry, Path
from geometry_msgs.msg import PoseStamped
from visualization_msgs.msg import MarkerArray
from std_msgs.msg import String

from rclpy.qos import QoSProfile, QoSDurabilityPolicy, QoSHistoryPolicy, QoSReliabilityPolicy

class my_node(Node):
    def __init__(self):
        super().__init__('demo1_node')

        
        qos_policy = QoSProfile(
            durability=QoSDurabilityPolicy.TRANSIENT_LOCAL,
            reliability=QoSReliabilityPolicy.RELIABLE,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=1
        )

        # Real wall clock — unaffected by Gazebo sim time
        self.wall_clock = Clock(clock_type=ClockType.STEADY_TIME)

        # States 
        self.started = False
        self.exploring = False
        self.returning = False
        self.return_timer_set = False
        self.start_attempts = 0

        # Record the real time when node started
        self.start_time = self.wall_clock.now()

        # 2 Path objects
        self.explorer_path = Path()
        self.explorer_path.header.frame_id = 'odom'

        self.home_path = Path()
        self.home_path.header.frame_id = 'odom'

        # --- Subscribers ---
        self.sub_map = self.create_subscription(
            OccupancyGrid, '/map', self.callback_map, qos_policy)

        self.sub_odom = self.create_subscription(
            Odometry, '/odom', self.callback_odom, 10)

        self.sub_stack = self.create_subscription(
            MarkerArray, '/stack_points', self.callback_stack_points, 10)

        # --- Publishers ---
        self.pub_slam_map = self.create_publisher(
            OccupancyGrid, '/ecte477/slam_map', qos_policy)

            
        self.pub_explorer = self.create_publisher(
            Path, '/ecte477/explorer', 10)
        
            
        self.pub_home = self.create_publisher(
            Path, '/ecte477/home', 10)

            
        self.pub_start = self.create_publisher(
            String, '/start_explore', 10)

            #Send Navigation goal to Nav2 (Go Home :) )
        self.pub_goal = self.create_publisher(
            PoseStamped, '/goal_pose', 10)

        
        #Timer
        self.start_timer = self.create_timer(
            1.0, self.check_start_time, clock=self.wall_clock)

        self.get_logger().info('demo1_node started! Will send start command in 15 seconds...')





    def check_start_time(self):
        
        elapsed = (self.wall_clock.now() - self.start_time).nanoseconds / 1e9

        if elapsed >= 15.0 and not self.started:
            msg = String()
            msg.data = 'start'
            self.pub_start.publish(msg)
            self.start_attempts += 1
            self.get_logger().info(f'Start command sent (attempt {self.start_attempts})...')

            if self.start_attempts >= 5:
                self.started = True
                self.exploring = True
                self.start_timer.cancel()
                self.get_logger().info('Exploration beginning!')




    def send_home_goal(self):
        goal = PoseStamped()
        goal.header.frame_id = 'map'
        goal.header.stamp = self.get_clock().now().to_msg()
        goal.pose.position.x = 0.0
        goal.pose.position.y = 0.0
        goal.pose.position.z = 0.0
        goal.pose.orientation.x = 0.0
        goal.pose.orientation.y = 0.0
        goal.pose.orientation.z = 0.0
        goal.pose.orientation.w = 1.0
        self.pub_goal.publish(goal)
        self.returning = True
        self.get_logger().info('Returning home to (0, 0, 0)!')




    def callback_map(self, data):
        self.pub_slam_map.publish(data)




    def callback_odom(self, data):
        pose = PoseStamped()
        pose.header = data.header
        pose.header.frame_id = 'odom'
        pose.pose = data.pose.pose

        if self.exploring:
            self.explorer_path.header.stamp = self.get_clock().now().to_msg()
            self.explorer_path.poses.append(pose)
            self.pub_explorer.publish(self.explorer_path)

        elif self.returning:
            self.home_path.header.stamp = self.get_clock().now().to_msg()
            self.home_path.poses.append(pose)
            self.pub_home.publish(self.home_path)




    def callback_stack_points(self, stack_points):
        if self.exploring and len(stack_points.markers) == 0 and not self.return_timer_set:
            self.exploring = False
            self.return_timer_set = True
            self.get_logger().info('Exploration complete! Returning home in 8 seconds...')
            self.return_start_time = self.wall_clock.now()
            self.return_timer = self.create_timer(
                1.0, self.check_return_time, clock=self.wall_clock)




    def check_return_time(self):
        elapsed = (self.wall_clock.now() - self.return_start_time).nanoseconds / 1e9
        if elapsed >= 8.0:
            self.return_timer.cancel()
            self.send_home_goal()


def main(args=None):
    rclpy.init(args=args)
    mn = my_node()
    rclpy.spin(mn)

if __name__ == '__main__':
    main()