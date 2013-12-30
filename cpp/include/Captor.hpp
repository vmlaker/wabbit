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

       @param  device     Device index.
       @param  width      Width of video.
       @param  height     Height of video.
       @param  duration   Duration of detection (in seconds.)
       @param  max_fps    Maximum FPS rate limit.
       @param  saver_queue      Link to the downstream disk saver worker.
    */
    Captor(
        const int& device, 
        const int& width,
        const int& height,
        const int& duration,
        const float& max_fps,
        bites::ConcurrentQueue <FrameAndTime>& saver_queue
        ):
        m_device        (device),
        m_width         (width),
        m_height        (height),
        m_duration      (duration),
        m_max_fps       (max_fps >= 0 ? max_fps : std::numeric_limits<float>::max()),
        m_saver_queue     (saver_queue)
        {/* Empty. */}

    /**
       Retrieve the current capture framerate.
    */
    std::vector <float> getFramerate ();

private:
    int m_device;
    int m_width;
    int m_height;
    int m_duration;
    float m_max_fps;

    // The output queue.
    bites::ConcurrentQueue <FrameAndTime>& m_saver_queue;

    // The current running framerate.
    bites::Mutexed <std::vector <float>> m_framerate;

    /**
       The threaded function.
    */
    void run();
};

}  // namespace wabbit.

#endif  // WABBIT_CAPTOR_HPP_INCLUDED
