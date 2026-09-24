import rclpy
from rclpy.node import Node
import time
from nav_msgs.msg import OccupancyGrid, Odometry, Path
from geometry_msgs.msg import PoseStamped
from visualization_msgs.msg import MarkerArray
from std_msgs.msg import String

from rclpy.qos import QoSProfile, QoSDurabilityPolicy, QoSHistoryPolicy, QoSReliabilityPolicy

class my_node(Node):
    def __init__(self):
        # Initialise subs, pubs, service calls, path object
        super().__init__('demo1_node')
        qos_policy = QoSProfile(durability=QoSDurabilityPolicy.TRANSIENT_LOCAL, reliability=QoSReliabilityPolicy.RELIABLE, history=QoSHistoryPolicy.KEEP_LAST, depth=1)


    def callback_map(self, data):
        # Do something with map

        
    def callback_odom(self, data):
        # Do something with odometry
       
        
    def callback_stack_points(self, stack_points):
        # Do something with stack_points array
      
	
# Main function
def main(args=None):
    rclpy.init(args=args)

    mn = my_node()

    rclpy.spin(mn)

if __name__ == '__main__':
    main()