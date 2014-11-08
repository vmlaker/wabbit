/**
   Record video frames to disk, and mark the timestamps in database.

   Parameters:  <duration_sec> [<config_file>]
 */

// Include standard headers.
#include <algorithm>
#include <sstream>
#include <string>
#include <vector>

// Include 3rd party headers
#include <opencv2/opencv.hpp>
#include <bites.hpp>

// Include application headers.
#include "Captor.hpp"
#include "DBWriter.hpp"
#include "DiskSaver.hpp"
#include "Deallocator.hpp"


/**
   Print the usage text.

   @param   argv0   Name of the command (e.g. argv[0])
*/
void usage(const char* argv0)
{
    std::list<std::string> usage = {
        "Usage: " + std::string(argv0) + " [options] duration [config_file]",
        "",
        "Options:",
        "    -v   produce verbose output",
    };
    for(auto ii=usage.begin(); ii!=usage.end(); ++ii){
        std::cout << *ii << std::endl;
    }
}

int main (int argc, char** argv)
{
    // Convert command-line arguments array (argv) into a vector of strings.
    std::vector<std::string> args(argv, argv + argc);

    // Extract command-line options.
    args.erase(args.begin());
    auto verbose = false;
    while (args.size() and args[0][0] == '-') {
        if(args[0] == "-v"){
            verbose = true;
            args.erase(args.begin());
        }else{
            break;
        }
        continue;
    }

    // With no command-line arguments, print the usage and bail.
    if (args.size() == 0)
    {
        usage(argv[0]);
        return 1;
    }

    // Extract command-line arguments DURATION and CONFIG_FILE.
    int DURATION;
    std::istringstream(args[0]) >> DURATION;
    args.erase(args.begin());
    std::string CONFIG_FILE = args.size() ? args[0] : "wabbit.cfg";
    if(verbose){
        std::cout << "duration    : " << DURATION << std::endl;
        std::cout << "config_file : " << CONFIG_FILE << std::endl;
    }
   
    // Load the configuration file.
    bites::Config config;
    if (not config.load(CONFIG_FILE)){
        std::cout << "Error: Failed to load " << CONFIG_FILE << std::endl;
        usage(argv[0]);
        return 1;
    }

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
        saver_queue,
        verbose ? &std::cout : NULL
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
