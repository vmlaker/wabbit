#ifndef WABBIT_IMAGEANDTIME_HPP_INCLUDED
#define WABBIT_IMAGEANDTIME_HPP_INCLUDED

#include <chrono>
#include <opencv2/opencv.hpp>

namespace wabbit {

/**
 *  Contains the image coupled with the capture time.
 */
struct ImageAndTime
{
    cv::Mat image;
    std::chrono::time_point< std::chrono::high_resolution_clock > time;
};

} // namespace wabbit

#endif //  WABBIT_IMAGEANDTIME_HPP_INCLUDED
