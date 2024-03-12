import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge

def publisher():
    cam = cv2.VideoCapture(0)
    br = CvBridge()
    pub = rospy.Publisher('/camera_image', Image, queue_size=10)
    rospy.init_node('camera_publisher')
    while not rospy.is_shutdown():
        ret, frame = cam.read()
        if ret == False:
            exit()
        cv2.imshow("Camera",frame)
        image_message = br.cv2_to_imgmsg(frame,"bgr8")
        pub.publish(image_message)
        key = cv2.waitKey(30)
        if key == ord("q"):
            break

if __name__ == '__main__':
    try:
        publisher()
    except rospy.ROSInterruptException:
        pass