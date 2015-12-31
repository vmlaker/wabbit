#ifndef WABBIT_IMAGEANDTIME_HPP_INCLUDED
#define WABBIT_IMAGEANDTIME_HPP_INCLUDED

#include <chrono>
#include <opencv2/opencv.hpp>

namespace wabbit {

// Contains the OpenCV image, coupled with the capture time and sequence number.
struct ImageAndTime
{
  cv::Mat image;
  typedef std::chrono::time_point< std::chrono::high_resolution_clock > time_point;
  time_point time;
  size_t sequence;
  ImageAndTime();
  ImageAndTime(const ImageAndTime&);
  ImageAndTime(const cv::Mat& image, const time_point& time, const size_t sequence);
};

}  // namespace wabbit

#endif  // WABBIT_IMAGEANDTIME_HPP_INCLUDED
