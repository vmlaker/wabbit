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
#include "DiskSaver.hpp"

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

    // Assign the displayer queue.
    bites::ConcurrentQueue <cv::Mat*> displayer_queue;
    captor.addOutput (displayer_queue);

    // Assign the saver queue.
    bites::ConcurrentQueue <cv::Mat*> saver_queue;
    captor.addOutput (saver_queue);

    // Create the global "done" queue.
    bites::ConcurrentQueue <cv::Mat*> done_queue;

    // Create the disk saver.
    sherlock::DiskSaver saver(
        config["pics_dir"],
        saver_queue,
        done_queue
        );

    // Create the output displayer.
    bites::ConcurrentQueue <sherlock::Classifier::RectColor> rect_colors;
    sherlock::Displayer displayer(
        displayer_queue,
        done_queue,
        rect_colors,
        captor
        );

    // Create the frame deallocation object.
    // The trigger count is 2, one each for displayer and disk saver.
    sherlock::Deallocator deallocator (done_queue);
    deallocator.setTrigger (2);

    // Start the threads.
    captor.start();
    saver.start();
    displayer.start();
    deallocator.start();

    // Join the threads.
    captor.join();
    saver.join();
    displayer.join();

    done_queue.push(NULL);
    deallocator.join();        
}
