import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from krish_messages.action import Fibonacci


class FibonacciClient(Node):
    def __init__(self):
        super().__init__('fibonacci_client')
        self.act_client = ActionClient(self, Fibonacci, 'gen_fibonacci_seq')

    def send_goal(self):
        print('Starting ROS Fibonacci Client Module')
        goal_msg = Fibonacci.Goal()
        goal_msg.order = 20
        self.act_client.wait_for_server()
        send_goal_to_server = self.act_client.send_goal_async(goal_msg)
        send_goal_to_server.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        get_result = goal_handle.get_result_async()
        get_result.add_done_callback(self.final_result_callback)

    def final_result_callback(self, result_future):
        final_result = result_future.result().result
        self.get_logger().info('Result: {}'.format(', '.join([str(n) for n in final_result.sequence])))
        rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    new_action_client = FibonacciClient()
    new_action_client.send_goal()

    rclpy.spin(new_action_client)


if __name__ == '__main__':
    main()
