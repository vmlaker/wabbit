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
#include <sherlock.hpp>

// Include application headers.
#include "Captor.hpp"
#include "DBWriter.hpp"
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

    /////////////////////////////////////////////////////////////////////
    //
    //  Assemble the pipeline:
    //
    //    captor  --+-->  disk saver  -->  DB writer  --+
    //              |                                   |
    //              +-->  displayer   ------------------+-->  deallocator
    //
    /////////////////////////////////////////////////////////////////////

    // Create the video capture object.
    wabbit::Captor captor(
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

    // Create the writer queue.
    bites::ConcurrentQueue <cv::Mat*> writer_queue;

    // Create the global deallocation queue.
    // Each thread will enqueue the frame
    // after it is finished processing the image.
    // The deallocation thread will free the frame memory
    // when every thread is finished with the given frame.
    bites::ConcurrentQueue <cv::Mat*> dealloc_queue;

    // Create the disk saver.
    wabbit::DiskSaver saver (
        config["pics_dir"],
        saver_queue,
        writer_queue,
        dealloc_queue
        );

    // Create the database writer.
    wabbit::DBWriter writer (
        writer_queue,
        dealloc_queue
        );

    // Create the output displayer.
    bites::ConcurrentQueue <sherlock::Classifier::RectColor> rect_colors;
    sherlock::Displayer displayer (
        displayer_queue,
        dealloc_queue,
        rect_colors,
        std::bind(&wabbit::Captor::getFramerate, &captor)
        );

    // Create the frame deallocation object.
    // The trigger count is 3, one each for:
    //    1) disk saver,
    //    2) database writer, and
    //    3) displayer.
    sherlock::Deallocator deallocator (dealloc_queue);
    deallocator.setTrigger (3);

    // Start the threads.
    captor.start();
    saver.start();
    writer.start();
    displayer.start();
    deallocator.start();

    // Join the threads.
    captor.join();
    saver.join();
    writer.join();
    displayer.join();

    dealloc_queue.push(NULL);
    deallocator.join();        
}
