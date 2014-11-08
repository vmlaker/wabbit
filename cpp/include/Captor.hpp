#ifndef WABBIT_CAPTOR_HPP_INCLUDED
#define WABBIT_CAPTOR_HPP_INCLUDED

// Include standard headers.
#include <vector>
#include <thread>
#include <mutex>
#include <limits>

// Include 3rd party headers.
#include <opencv2/opencv.hpp>
#include <bites.hpp>

namespace wabbit {

/**
   Video capture thread.
*/
class Captor : public bites::Thread 
{
public:
    /**
       Encapsulates pointer to video frame and time of capture.
    */
    typedef std::pair < 
        cv::Mat*, std::chrono::time_point <
            std::chrono::high_resolution_clock 
            > 
        > FrameAndTime;

    /**
       Initialize the video capture thread with parameters.

       @param  config         Application configuration.
       @param  duration       Duration of detection (in seconds.)
       @param  output_queue   Link to the downstream queue.
       @param  output_stream  Optional output stream for verbose output.
    */
    Captor(
        bites::Config& config,
        const int& duration,
        bites::ConcurrentQueue <FrameAndTime>& output_queue,
        std::ostream* output_stream = NULL
        ):
        m_config       (config),
        m_duration     (duration),
        m_output_queue (output_queue),
        m_output_stream (output_stream)
        {/* Empty. */}

    /**
       Retrieve the current capture framerate.
    */
    std::vector <float> getFramerate ();

private:
    // Application configuration.
    bites::Config& m_config;

    // Duration for video capture.
    int m_duration;

    // The output queue.
    bites::ConcurrentQueue <FrameAndTime>& m_output_queue;

    // The output stream used for verbose output.
    std::ostream* m_output_stream;

    // The current running framerate.
    bites::Mutexed <std::vector <float>> m_framerate;

    /**
       The threaded function.
    */
    void run();
};

}  // namespace wabbit.

#endif  // WABBIT_CAPTOR_HPP_INCLUDED
