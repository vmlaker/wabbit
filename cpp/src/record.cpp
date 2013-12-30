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
    //    captor  -->  disk saver  -->  DB writer  -->  deallocator
    //
    /////////////////////////////////////////////////////////////////////

    // Create the queues.
    bites::ConcurrentQueue <wabbit::Captor::FrameAndTime> saver_queue;
    bites::ConcurrentQueue <wabbit::Captor::FrameAndTime> writer_queue;

    // Create the global deallocation queue.
    // Each thread will enqueue the frame
    // after it is finished processing the image.
    // The deallocation thread will free the frame memory
    // when every thread is finished with the given frame.
    bites::ConcurrentQueue <cv::Mat*> dealloc_queue;

    // Create the video capture object.
    wabbit::Captor captor(
        config,
        DURATION,
        saver_queue
        );

    // Create the disk saver.
    wabbit::DiskSaver saver (
        config["pics_dir"],
        saver_queue,
        writer_queue,
        dealloc_queue
        );

    // Create the database writer.
    wabbit::DBWriter writer (
        config,
        writer_queue,
        dealloc_queue
        );

    // Create the frame deallocation object.
    // The trigger count is 2, one each for:
    //    1) disk saver, and
    //    2) database writer.
    sherlock::Deallocator deallocator (dealloc_queue);
    deallocator.setTrigger (2);

    // Start the threads.
    captor.start();
    saver.start();
    writer.start();
    deallocator.start();

    // Join the threads.
    captor.join();
    saver.join();
    writer.join();

    dealloc_queue.push(NULL);
    deallocator.join();        
}
