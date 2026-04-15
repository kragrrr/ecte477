import rclpy
import sys
from rclpy.node import Node
from krish_messages.srv import AddTwoInts


class AddTwoIntsClient(Node):
    def __init__(self):
        super().__init__('add_two_ints_client')
        self.client = self.create_client(AddTwoInts, 'add_two_ints')
        while not self.client.wait_for_service(timeout_sec=1.0):
            print('Waiting for server ...... ')
        self.request = AddTwoInts.Request()

    def send_request(self, num1, num2):
        self.request.a = num1
        self.request.b = num2
        self.result = self.client.call_async(self.request)
        rclpy.spin_until_future_complete(self, self.result)
        return self.result.result()


def main():
    if len(sys.argv) == 3:
        x = int(sys.argv[1])
        y = int(sys.argv[2])
    else:
        print('USAGE: add_two_ints_client x y')
        sys.exit(1)

    rclpy.init(args=None)

    new_client = AddTwoIntsClient()
    response = new_client.send_request(x, y)
    print('%s + %s = %s' % (x, y, response.sum))

    new_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
