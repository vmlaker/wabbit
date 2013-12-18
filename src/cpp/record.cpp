/**
   Record video frames to disk, and mark the timestamps in database.

   Parameters:  <duration_sec> [<config_file>]
 */

// Include standard headers.
#include <string>
#include <sstream>

// Include 3rd party headers
#include <opencv2/opencv.hpp>
#include <bites.hpp>

int main (int argc, char** argv)
{
    if (argc == 1)
    {
        std::cout << "Usage: " << argv[0] << " duration [config_file]" << std::endl;
        exit(1);
    }

    // Parse command-line arguments.
    int DURATION;
    std::istringstream(std::string(argv[1])) >> DURATION;
    std::string CONFIG = argc >= 3 ? argv[2] : "wabbit.cfg";

    // Load the configuration file.
    bites::Config config (CONFIG);

    // Create the OpenCV video capture object.
    cv::VideoCapture cap(atoi(config["device"].c_str()));
    cap.set(3, atoi(config["width"].c_str()));
    cap.set(4, atoi(config["height"].c_str()));

    // Monitor framerates for the given seconds past.
    bites::RateTicker ticker ({ 2, 5, 10 });

    // Go into main loop.
    auto prev = boost::posix_time::microsec_clock::universal_time();
    auto interval_float = 1/atof(config["max_fps"].c_str());
    int interval_sec = (int) interval_float;
    auto min_interval = boost::posix_time::time_duration(
        0, // Hours.
        0, // Minutes.
        interval_sec, // Seconds.
        (interval_float - interval_sec) * 1000000  // Fractional seconds.
        );
    auto end = prev + boost::posix_time::seconds(DURATION);
    while (end > boost::posix_time::microsec_clock::universal_time() or DURATION < 0)
    {
        // Insert delay to observe maximum framerate limit.
        auto elapsed = boost::posix_time::microsec_clock::universal_time() - prev;
        auto sleep_microsec = ( min_interval - elapsed ).total_microseconds();
        sleep_microsec = std::max( long(0), sleep_microsec );
        usleep(sleep_microsec);
        prev = boost::posix_time::microsec_clock::universal_time();

        // Take a snapshot.
        auto frame = new cv::Mat;
        cap >> *frame; 

        // Set the framerate.
        auto fps = ticker.tick();
        std::cout << std::fixed << std::setprecision(2);
        std::cout << fps[0] << ", " << fps[1] << ", " << fps[2] << std::endl;
        
        delete frame;
    }
}
