import tf
import rospy
from sensor_msgs.msg import Image, CameraInfo
from tf.transformations import quaternion_from_euler, euler_from_quaternion
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from cv_bridge import CvBridge
import cv2
import numpy as np
import math

class DepthToDistanceConverter:
    def __init__(self):
        self.bridge = CvBridge()

        # Subscribe to depth image and camera info topics
        self.depth_sub = rospy.Subscriber('/zed2/depth/depth_registered', Image, self.depth_callback)
        self.camera_info_sub = rospy.Subscriber('/zed2/depth/camera_info', CameraInfo, self.camera_info_callback)

        self.camera_info = None
        self.depth_image = None

    def camera_info_callback(self, msg):
        self.camera_info = msg

    def depth_callback(self, msg):
        self.depth_image = self.bridge.imgmsg_to_cv2(msg)

    def get_distance_at_point(self, x, y):
        if self.depth_image is None or self.camera_info is None:
            rospy.logwarn("Depth image or camera info not available yet.")
            return None

        fx = self.camera_info.K[0]  # focal length in x-direction
        fy = self.camera_info.K[4]  # focal length in y-direction
        cx = self.camera_info.K[2]  # principal point x-coordinate
        cy = self.camera_info.K[5]  # principal point y-coordinate

        depth_value = self.depth_image[y, x]  # Depth value at the given pixel

        # Compute distance using the pinhole camera model
        distance = depth_value / np.sqrt((fx ** 2) + (fy ** 2))
        return distance * 1000

class DepthAndIMUController:
    def __init__(self):
        self.converter = DepthToDistanceConverter()
        self.orientation_z = 0.0  # Initial value
        self.initial_orientation = 0.0
        self.current_orientation = 0.0
        self.current_location = None

        # Subscribe to Odometry and IMU data
        self.odom_sub = rospy.Subscriber('/ground_truth', Odometry, self.odom_callback)

    def odom_callback(self, odom_msg):
        x = odom_msg.pose.pose.position.x
        y = odom_msg.pose.pose.position.y

        # Retrieve the current orientation (theta)
        quaternion = (
            odom_msg.pose.pose.orientation.x,
            odom_msg.pose.pose.orientation.y,
            odom_msg.pose.pose.orientation.z,
            odom_msg.pose.pose.orientation.w
        )
        euler = tf.transformations.euler_from_quaternion(quaternion)
        theta = euler[2]

        # Update the current location
        self.current_location = (x, y, theta)

    def set_initial_orientation(self):
        self.initial_orientation = self.orientation_z

    def update_current_orientation(self):
        self.current_orientation = self.orientation_z

    def get_rotation_angle(self):
        return abs(self.current_orientation - self.initial_orientation)  # Absolute difference in orientation

class MovementController:
    def __init__(self):
        self.pub = rospy.Publisher('/gazebo/controllers/diff_drive/cmd_vel', Twist, queue_size=10)
        self.wall_detected = False  # Flag to indicate if wall has been detected


    def forward(self):
        twist_msg = Twist()
        twist_msg.linear.x = 1
        twist_msg.angular.z = 0
        self.pub.publish(twist_msg)

    def rotate_left(self):
        twist_msg = Twist()
        twist_msg.angular.z = 1.0  # Adjust the angular velocity as needed for a 90-degree turn
        twist_msg.linear.x = 0
        self.pub.publish(twist_msg)

    def rotate_right(self):
        twist_msg = Twist()
        twist_msg.angular.z = -1.0  # Adjust the angular velocity as needed for a 90-degree turn
        twist_msg.linear.x = 0
        self.pub.publish(twist_msg)     

    def stop(self):
        twist_msg = Twist()
        twist_msg.linear.x = 0
        twist_msg.angular.z = 0
        self.pub.publish(twist_msg)

def depth(controller):
    if controller.converter.depth_image is not None and controller.converter.camera_info is not None:
            # Get distance at the center of the image
            image_height, image_width = controller.converter.depth_image.shape[:2]
            center_x = image_width // 2
            center_y = image_height // 2

            distance_at_center = controller.converter.get_distance_at_point(center_x, center_y)
            return(distance_at_center)





if __name__ == '__main__':
     controller = DepthAndIMUController()    #object to get positon and depth values

     movement_controller = MovementController()  #object to control rovers motions










#     controller = DepthAndIMUController()    object to get positon and depth values

#     movement_controller = MovementController()  object to control rovers motions


#     (controller.current_location) 
#     a tuple with values x,y,theta(rotation angle) from the ground truth


#     depth(controller)
#     returns depth as a float



#     movement_controller.rotate_right()   to move right
#     movement_controller.rotate_left()    to move left
#     movement_controller.forward()        to move forward
#     movement_controller.stop()           to move left










