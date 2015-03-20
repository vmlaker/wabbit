// Include application headers.
#include "Display.hpp"

namespace wabbit {

Display::Display( )
{
    cv::namedWindow( "Hello", cv::WINDOW_AUTOSIZE );
}

wabbit::ImageAndTime* 
Display::operator()( wabbit::ImageAndTime* image_and_time )
{
    cv::imshow( "Hello", image_and_time->image );
    cv::waitKey( 1 );
    return image_and_time;
}

}  // namespace wabbit.
