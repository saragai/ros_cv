#include <ros/ros.h>
#include <image_transport/image_transport.h>
#include <cv_bridge/cv_bridge.h>
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/features2d/features2d.hpp"
#include "opencv2/core/core.hpp"
#include "opencv2/imgproc/imgproc.hpp"

class MyCvFC
{
	image_transport::Subscriber img_sub_;
	image_transport::ImageTransport it_;
	void imageCallback(const sensor_msgs::ImageConstPtr &msg){
		ROS_INFO("Recieve image");
		//convert from ROS message to OpenCV object
		cv::Mat in_img = cv_bridge::toCvCopy(msg, msg->encoding)->image;
		
		//write opencv code
		cv::Mat dst_img, work_img;
		dst_img = in_img.clone();
		work_img = in_img.clone();
		printf("here");
		//cv::cvtColor(in_img, work_img, CV_BGR2GRAY);
		
		//Preprocess for Hough
		cv::GaussianBlur(work_img, work_img, cv::Size(11,11),2,2);

		//Detect Circle using Hough
		std::vector<cv::Vec3f> circles;
		cv::HoughCircles(work_img, circles, CV_HOUGH_GRADIENT, 1, 100, 20, 50);
		std::vector<cv::Vec3f>::iterator it = circles.begin();
		for(;it!=circles.end();++it){
			cv::Point center(
				cv::saturate_cast<int>((*it)[0]), 
				cv::saturate_cast<int>((*it)[1])
			);
			int radius = cv::saturate_cast<int>((*it)[2]);
			cv::circle(dst_img, center, radius, cv::Scalar(0,0,255),2);
		}
		cv::imshow("FindCircle", dst_img);
		cv::waitKey(1);
		//end opencv code
	}
	public:
	MyCvFC(ros::NodeHandle nh = ros::NodeHandle()) : it_(nh)
	{
		img_sub_= it_.subscribe("image", 3, &MyCvFC::imageCallback, this);
		cv::namedWindow("FindCircle", 1);
	}
};

int main(int argc, char **argv)
{
	ros::init(argc, argv, "my_cv_findcircle_node");
	MyCvFC mcFC;
	ros::spin();
}

