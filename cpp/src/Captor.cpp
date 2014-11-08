// Include standard headers.
#include <iomanip>

// Include 3rd party headers.
#include <bites.hpp>

// Include application headers.
#include "Captor.hpp"

namespace wabbit {

std::vector <float> Captor::getFramerate ()
{
    return m_framerate.get();
}

void Captor::run ()
{
    // Create the OpenCV video capture object.
    cv::VideoCapture cap(atoi(m_config["device"].c_str()));
    cap.set(3, atoi(m_config["width"].c_str()));
    cap.set(4, atoi(m_config["height"].c_str()));

    // Monitor framerates for the given seconds past.
    bites::RateTicker ticker ({ 1, 5, 10 });

    // Compute interval needed to observe maximum FPS limit.
    float max_fps = atof(m_config["max_fps"].c_str());
    max_fps = max_fps >= 0 ? max_fps : std::numeric_limits<float>::max();
    float interval_seconds = 1 / max_fps;
    int interval_ms = interval_seconds * 1000000;
    auto min_interval = std::chrono::microseconds( interval_ms );

    // Set the minimum read time for detecting camera disconnect.
    int min_read_ms = atof(m_config["min_read"].c_str()) * 1000000;
    
    // Run the loop under the following conditions:
    //   1) designated amount of time hasn't expired 
    //      or was given as negative amount, and
    //   2) capture device is opened.
    auto prev = std::chrono::system_clock::now();
    auto end = prev + std::chrono::seconds(m_duration);
    while ((end > std::chrono::system_clock::now() or m_duration < 0) and cap.isOpened())
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
        // The only way I could detect camera disconnect was by
        // thresholding the length of time to call read() method;
        // for some reason return value of read() is always True, 
        // even after disconnecting the camera.
        auto frame = new cv::Mat;
        auto begin = std::chrono::system_clock::now();
        cap >> *frame; 
        elapsed = std::chrono::system_clock::now() - begin;
        elapsed_ms = std::chrono::duration_cast<std::chrono::microseconds> (elapsed);
        if (elapsed_ms.count() < min_read_ms)
        {
            // TODO: Write error to log instead of stdout.
            std::cout << "Read time failed to meet threshold, "
                      << elapsed_ms.count() << " < " 
                      << min_read_ms << std::endl;
            break;
        }

        // Set the framerate.
        auto fps = ticker.tick();
        m_framerate.set(fps);

        // Optionally print the current framerate.
        if(m_output_stream){
            for(auto ii=fps.begin(); ii!=fps.end(); ++ii){
                *m_output_stream << std::fixed << std::setw(7) << std::setprecision(2) << *ii;
            }
            *m_output_stream << std::endl;
        }

        // Push image onto output queue.
        Captor::FrameAndTime fat (frame, prev);
        m_output_queue.push (fat);
    }

    // Signal end-of-processing by pushing NULL onto output queue.
    Captor::FrameAndTime fat (NULL, prev);
    m_output_queue.push (fat);
}

}  // namespace wabbit.
