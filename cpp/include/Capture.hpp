#ifndef WABBIT_CAPTURE_HPP_INCLUDED
#define WABBIT_CAPTURE_HPP_INCLUDED

// Include standard headers.
#include <vector>

// Include 3rd party headers.
#include <opencv2/opencv.hpp>
#include <bites.hpp>

// Include application headers.
#include "ImageAndTime.hpp"

namespace wabbit {

/**
 *  Video capture stage.
 */
class Capture
{
public:

    /**
     *  Initialize the video capture stage with given parameters.
     *
     *  @param  config         Application configuration.
     *  @param  duration       Duration of detection (in seconds.)
     *  @param  output_stream  Optional output stream for verbose output.
    */
    Capture( bites::Config& config,
             const int& duration,
             std::ostream* output_stream = NULL );

    /**
     *  Copy-ctor needed for TBB.
     */
    Capture( const Capture& );
    
    /**
     *  Retrieve the current capture framerate.
     */
    std::vector <float> getFramerate ();

    /**
     * The function operator called by TBB.
     */
    bool operator()( wabbit::ImageAndTime*& );

private:
    // Application configuration.
    bites::Config& m_config;

    // Duration for video capture.
    int m_duration;

    // The output stream used for verbose output.
    std::ostream* m_output_stream;

    // The current running framerate.
    bites::Mutexed <std::vector <float>> m_framerate;

    // OpenCV video capture object.
    cv::VideoCapture m_video_capture;

    // Monitor framerates for the given seconds past.
    bites::RateTicker m_rate_ticker;

    // Variables to observe configured framerate.
    std::chrono::system_clock::time_point m_prev_time;
    std::chrono::system_clock::time_point m_end_time;
    std::chrono::microseconds m_min_interval;

    // Minimum read time to detect camera connectivity.
    float m_min_read;

};

}  // namespace wabbit.

#endif  // WABBIT_CAPTURE_HPP_INCLUDED
