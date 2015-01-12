// Include application headers.
#include "Deallocate.hpp"

namespace wabbit {

wabbit::ImageAndTime* 
Deallocate::operator()( wabbit::ImageAndTime* image_and_time )
{
    delete image_and_time;
    return NULL;
}

}  // namespace wabbit.
