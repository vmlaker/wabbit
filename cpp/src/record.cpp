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
#include "DBWriter.hpp"
#include "DiskSaver.hpp"
#include "Deallocator.hpp"

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
    //    captor  -->  disk saver(s)  -->  DB writer(s)  -->  deallocator
    //
    /////////////////////////////////////////////////////////////////////

    // Create the queues.
    bites::ConcurrentQueue <wabbit::Captor::FrameAndTime> saver_queue;
    bites::ConcurrentQueue <wabbit::Captor::FrameAndTime> writer_queue;
    bites::ConcurrentQueue <cv::Mat*> dealloc_queue;

    // Create the video capture object.
    wabbit::Captor captor(
        config,
        DURATION,
        saver_queue
        );

    // Contain disk saver and DB writer threads in a common list.
    std::list <bites::Thread*> threads;

    // Create the disk savers.
    for (int ii=0; ii<atoi(config["num_savers"].c_str()); ++ii)
    {
        // Create the disk saver.
        auto saver = new wabbit::DiskSaver (
            config["pics_dir"],
            saver_queue,
            writer_queue
            );
        threads.push_back (saver);
    }

    // Create the database writers.
    for (int ii=0; ii<atoi(config["num_writers"].c_str()); ++ii)
    {
        // Create the database writer.
        auto writer = new wabbit::DBWriter (
            config,
            writer_queue,
            dealloc_queue
            );
        threads.push_back (writer);
    }

    // Create the frame deallocation object.
    wabbit::Deallocator deallocator (dealloc_queue);

    // Start the threads.
    captor.start();
    for (auto thread : threads) thread->start();
    deallocator.start();

    // Join the threads.
    captor.join();
    for (auto thread : threads) thread->join();
    deallocator.join();        

    // Delete the allocated thread objects.
    for (auto thread : threads) delete thread;
}
