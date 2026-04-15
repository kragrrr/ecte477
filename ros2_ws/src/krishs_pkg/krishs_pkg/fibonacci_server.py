import rclpy
import time
from rclpy.node import Node
from rclpy.action import ActionServer
from krish_messages.action import Fibonacci


class FibonacciServer(Node):
    def __init__(self):
        super().__init__('fibonacci_server')
        self.act_srv = ActionServer(self, Fibonacci, 'gen_fibonacci_seq', self.fib_callback)
        self.feedback = Fibonacci.Feedback()
        self.result = Fibonacci.Result()

    def fib_callback(self, goal):
        goal.succeed()
        print('Starting ROS Fibonacci Server Module')
        self.feedback.sequence = []
        self.feedback.sequence.append(0)
        self.feedback.sequence.append(1)
        self.get_logger().info(
            'Creating Fibonacci sequence of order %s with seeds %s, %s'
            % (goal.request.order, self.feedback.sequence[0], self.feedback.sequence[1])
        )

        for i in range(1, goal.request.order):
            self.feedback.sequence.append(self.feedback.sequence[i - 1] + self.feedback.sequence[i])
            goal.publish_feedback(self.feedback)
            time.sleep(1)

        self.get_logger().info('Succeeded')
        self.result.sequence = self.feedback.sequence
        return self.result


def main(args=None):
    rclpy.init(args=args)
    new_action_server = FibonacciServer()
    rclpy.spin(new_action_server)


if __name__ == '__main__':
    main()
