/*
 *  Resize.cpp
 *
 */

#include <opencv2/opencv.hpp>
#include <bites.hpp>

#include "Resize.hpp"

namespace wabbit {

Resize::Resize( bites::Config& config )
    : m_config( config ){}

Resize::Resize( const Resize& resize )
    : m_config( resize.m_config ){}

wabbit::ImageAndTime 
Resize::operator()( const wabbit::ImageAndTime& image_and_time )
{
    cv::Mat image2;
    cv::Size size( stod(m_config["width2"]), stod(m_config["height2"]) );
    cv::resize( image_and_time.image, image2, size, 0, 0, cv::INTER_AREA );
    return ImageAndTime( image2, image_and_time.time, image_and_time.sequence );
}

}  // namespace wabbit.
