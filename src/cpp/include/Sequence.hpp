#ifndef WABBIT_SEQUENCE_HPP_INCLUDED
#define WABBIT_SEQUENCE_HPP_INCLUDED

#include "ImageAndTime.hpp"

namespace wabbit {

class Sequence {
public:
  const size_t operator()( const ImageAndTime& image_and_time ){
    return image_and_time.sequence;
  }
};

}  // namespace wabbit

#endif  // WABBIT_SEQUENCE_HPP_INCLUDED
