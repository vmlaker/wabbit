#include "ImageAndTime.hpp"

namespace wabbit {
  
ImageAndTime::ImageAndTime()
  : image(), time(), sequence(-1) {};

ImageAndTime::ImageAndTime(const ImageAndTime& image_and_time)
  : image(image_and_time.image),
    time(image_and_time.time),
    sequence(image_and_time.sequence) {};

ImageAndTime::ImageAndTime(const cv::Mat& image, const time_point& time, const size_t sequence)
  : image(image), time(time), sequence(sequence) {};

}  // namespace wabbit.
