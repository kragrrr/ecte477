import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped
from sensor_msgs.msg import LaserScan


class MoveToWall(Node):
    def __init__(self):
        super().__init__('move_to_wall')
        self.publisher = self.create_publisher(TwistStamped, '/cmd_vel', 10)
        self.subscription = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        self.cmd = TwistStamped()
        self.target_distance = 1.0

    def scan_callback(self, msg):
        front = msg.ranges[0]
        if front > self.target_distance:
            self.cmd.twist.linear.x = 0.2
            self.cmd.twist.angular.z = 0.0
        else:
            self.cmd.twist.linear.x = 0.0
            self.cmd.twist.angular.z = 0.0
        self.publisher.publish(self.cmd)


def main(args=None):
    rclpy.init(args=args)
    node = MoveToWall()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
