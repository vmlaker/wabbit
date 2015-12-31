#ifndef WABBIT_IMAGEANDTIME_HPP_INCLUDED
#define WABBIT_IMAGEANDTIME_HPP_INCLUDED

#include <chrono>
#include <opencv2/opencv.hpp>

namespace wabbit {

// Contains the OpenCV image, coupled with the capture time and sequence number.
struct ImageAndTime
{
  typedef std::chrono::time_point< std::chrono::high_resolution_clock > time_point;

  cv::Mat image;
  time_point time;
  size_t sequence;
  ImageAndTime(): image(), time(), sequence(0) {};
  ImageAndTime(const cv::Mat& image, const time_point& time, const size_t sequence)
    : image(image), time(time), sequence(sequence) {};
  static size_t s_sequence;
};

}  // namespace wabbit

#endif  // WABBIT_IMAGEANDTIME_HPP_INCLUDED
