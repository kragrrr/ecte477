import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point


class MyPublisher(Node):
    def __init__(self):
        # setup node and publisher
        super().__init__('robot_location_publisher')
        self.pub = self.create_publisher(Point, 'robot_location', 10)
        # initialise the location of the robot
        self.location = Point()
        self.location.x = 10.0
        self.location.y = 10.0
        self.location.z = 10.0
        # setup a timer to update the position at a rate of 10 Hz
        timer_period = 0.1
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        # publish location
        self.pub.publish(self.location)
        self.get_logger().info('Publishing location: %f, %f' % (self.location.x, self.location.y))
        # Simulate a move
        self.location.x += 1.0
        self.location.y += 2.0


def main(args=None):
    rclpy.init(args=args)
    robot_publisher = MyPublisher()
    rclpy.spin(robot_publisher)


if __name__ == '__main__':
    main()
