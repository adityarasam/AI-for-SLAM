import sys, time

# numpy and scipy
import numpy as np

import cv2
import matplotlib.pyplot as plt
#from scipy.ndimage import filters



# Ros libraries
import roslib
import rospy
from cv_bridge import CvBridge, CvBridgeError
# Ros Messages
from sensor_msgs.msg import CompressedImage


bridge = CvBridge()

def grey(image):
    return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
def gauss(image):
    return cv2.GaussianBlur(image, (5, 5), 0)
def canny(image):
    edges = cv2.Canny(image,50,100)
    
    return edges


def draw_point(u,v,img):
    center_coordinates = (int(u),int(v))
 
    # Radius of circle
    radius = 2
    
    # Blue color in BGR
    color = (255, 0, 0)
    
    # Line thickness of 2 px
    thickness = 3
    
    # Using cv2.circle() method
    # Draw a circle with blue line borders of thickness of 2 px
    img = cv2.circle(img, center_coordinates, radius, color, thickness)

    return img


def scene_geometry(img):
    camera_height=1
    Z=1
    umax = img.shape[0]
    vmax= img.shape[1]
    fx=320
    fy=240
    cx=320
    cy=240
    X=0.5
    Y=0

    u=(fx*X)/Z+cx
    v=(fy*Y)/Z+cy
    print("v,u", v,u)
    print("img[v,u]",img[int(v),int(u)])
    #img[int(v),int(u)] = 252
    img = draw_point(u,v,img)
    

    return img






def callback(ros_data):
    '''Callback function of subscribed topic. 
    Here images get converted and features detected'''


    #----------Receive 

   
    try:
        image_np = bridge.compressed_imgmsg_to_cv2(ros_data,"bgr8")
    except CvBridgeError, e:
        print(e)


    #----------Process
    copy = np.copy(image_np)
    #grey1 = grey(copy)
    gaus = gauss(copy)
    edges = canny(gaus)


    #----------Publish
    msg = CompressedImage()
    msg.header.stamp = rospy.Time.now()
    msg.format = "jpeg"
    msg.data = np.array(cv2.imencode('.jpg', edges)[1]).tostring()
    # Publish new image
    image_pub.publish(msg)


def main_ros():
    subscriber = rospy.Subscriber("/camera/image_raw/compressed",CompressedImage, callback,  queue_size = 10)
    rospy.init_node('line_detector', anonymous=True)

    image_pub = rospy.Publisher("/line_detect/image_raw/compressed",CompressedImage)

    try:
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down ROS Image feature detector module"

    
    
    
if __name__ == '__main__':
    #main_ros(sys.argv)
    #main_ros()

    subscriber = rospy.Subscriber("/camera/image_raw/compressed",CompressedImage, callback,  queue_size = 10)
    rospy.init_node('line_detector', anonymous=True)

    image_pub = rospy.Publisher("/line_detect/image_raw/compressed",CompressedImage)

    try:
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down ROS Image feature detector module"




    '''
    img = cv2.imread("image.png",0)
    print(img.shape)
    img = scene_geometry(img)
    cv2.imshow('Image',img)
    cv2.waitKey(0)'''
    #cv2.destroyAllWindows()
