/**
   Record video frames to disk, and mark the timestamps in database.

   Parameters:  <duration_sec> [<config_file>]
 */

// Include standard headers.
#include <string>
#include <sstream>
#include <algorithm>

// Include 3rd party headers
#include <opencv2/opencv.hpp>
#include <bites.hpp>

// Include application headers.
#include "Captor.hpp"
#include "Classifier.hpp"
#include "Deallocator.hpp"
#include "Displayer.hpp"

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

    // Create the video capture object.
    sherlock::Captor captor(
        (int)atoi(config["device"].c_str()),
        (int)atoi(config["width"].c_str()),
        (int)atoi(config["height"].c_str()),
        DURATION,
        (float)atoi(config["max_fps"].c_str())
        );

    // Assign the capture output queue.
    bites::ConcurrentQueue <cv::Mat*> frame_queue;
    captor.addOutput (frame_queue);

    // Create the output displayer.
    bites::ConcurrentQueue <sherlock::Classifier::RectColor> rect_colors;
    bites::ConcurrentQueue <cv::Mat*> done_queue;
    sherlock::Displayer displayer(
        frame_queue,
        done_queue,
        rect_colors,
        captor
        );

    // Create the frame deallocation object.
    sherlock::Deallocator deallocator (done_queue);
    deallocator.setTrigger (1);

    // Start the threads.
    captor.start();
    displayer.start();
    deallocator.start();

    // Join the threads.
    captor.join();
    displayer.join();

    done_queue.push(NULL);
    deallocator.join();        
}
