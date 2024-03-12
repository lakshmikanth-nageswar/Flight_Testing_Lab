import rospy 
from sensor_msgs import point_cloud2

def lidar_callback(msg):
    ## Filter the Noisy data 
    pub.publish(msg)

if __name__ == '__main__':
    rospy.init_node('lidar_to_rtabmap_node')
    
    # Subscribe to the LiDAR topic
    rospy.Subscriber('/lidar_topic', point_cloud2, lidar_callback)
    
    # Publish to RTAB-Map topic
    pub = rospy.Publisher('/rtabmap/cloud_map', point_cloud2, queue_size=10)
    
    rospy.spin()
