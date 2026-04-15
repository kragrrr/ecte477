import rclpy
from rclpy.node import Node
from krish_messages.srv import AddTwoInts


class AddTwoIntsServer(Node):
    def __init__(self):
        super().__init__('add_two_ints_server')
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.handle_add_two_ints)
        print('Ready to add two ints')

    def handle_add_two_ints(self, request, response):
        response.sum = request.a + request.b
        print('Returning to client: %s + %s = %s' % (request.a, request.b, response.sum))
        return response


def main(args=None):
    rclpy.init(args=args)
    new_server = AddTwoIntsServer()
    rclpy.spin(new_server)


if __name__ == '__main__':
    main()
