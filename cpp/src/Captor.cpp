// Include 3rd party headers.
#include <bites.hpp>

// Include application headers.
#include "Captor.hpp"

namespace wabbit {

void Captor::pushOutput (FrameAndTime& fat)
{
    m_displayer_queue.push (fat.first);
    m_saver_queue.push (fat);
}

std::vector <float> Captor::getFramerate ()
{
    return m_framerate.get();
}

void Captor::run ()
{
    // Create the OpenCV video capture object.
    cv::VideoCapture cap(m_device);
    cap.set(3, m_width);
    cap.set(4, m_height);

    // Monitor framerates for the given seconds past.
    bites::RateTicker ticker ({ 1, 5, 10 });

    // Compute interval needed to observe maximum FPS limit.
    float interval_seconds = 1 / m_max_fps;
    int interval_ms = interval_seconds * 1000000;
    auto min_interval = std::chrono::microseconds( interval_ms );

    // Run the loop for designated amount of time.
    auto prev = std::chrono::system_clock::now();
    auto end = prev + std::chrono::seconds(m_duration);
    while (end > std::chrono::system_clock::now())
    {
        // Insert delay to observe maximum framerate limit.
        auto elapsed = std::chrono::system_clock::now() - prev;
        auto elapsed_ms = 
            std::chrono::duration_cast<std::chrono::microseconds> (elapsed);
        auto sleep_ms = min_interval - elapsed_ms;
	sleep_ms = sleep_ms.count() < 0 ? std::chrono::microseconds(0) : sleep_ms;
        usleep(sleep_ms.count());
        prev = std::chrono::system_clock::now();            

        // Take a snapshot.
        auto frame = new cv::Mat;
        cap >> *frame; 

        // Set the framerate.
        m_framerate.set(ticker.tick());

        // Push image onto all output queues.
        Captor::FrameAndTime fat (frame, prev);
        pushOutput (fat);
    }

    // Signal end-of-processing by pushing NULL onto all output queues.
    Captor::FrameAndTime fat (NULL, prev);
    pushOutput (fat);
}

}  // namespace wabbit.
