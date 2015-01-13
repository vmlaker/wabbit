/**
 *  Record video frames to disk, and mark the timestamps in database.
 *
 *  Parameters:  <duration_sec> [<config_file>]
 */

// Include standard headers.
#include <algorithm>
#include <sstream>
#include <string>
#include <vector>

// Include 3rd party headers
#include <opencv2/opencv.hpp>
#include <bites.hpp>
#include "tbb/flow_graph.h"

// Include application headers.
#include "Capture.hpp"
#include "Display.hpp"
#include "DiskWrite.hpp"
#include "DBWrite.hpp"

using namespace tbb::flow;

/*
 *  Print the usage text.
 *
 *  @param  argv0  Name of the command (e.g. argv[0])
 */
void usage( const char* argv0 )
{
    std::list<std::string> usage = {
        "Usage: " + std::string( argv0 ) + " [options] duration [config_file]",
        "",
        "Options:",
        "    -v   produce verbose output",
    };
    for( auto ii=begin(usage); ii!=end(usage); ++ii ){
        std::cout << *ii << std::endl;
    }
}

int main( int argc, char** argv )
{
    // Convert command-line arguments array (argv) into a vector of strings.
    std::vector<std::string> args( argv, argv + argc );

    // Extract command-line options.
    args.erase( args.begin() );
    auto verbose = false;
    while( args.size() and args[0][0] == '-' ){
        if( args[0] == "-v" ){
            verbose = true;
            args.erase( args.begin() );
        }else{
            break;
        }
        continue;
    }

    // With no command-line arguments, print the usage and bail.
    if( args.size() == 0 )
    {
        usage( argv[0] );
        return 1;
    }

    // Extract command-line arguments DURATION and CONFIG_FILE.
    int DURATION;
    std::istringstream( args[0] ) >> DURATION;
    args.erase( args.begin() );
    std::string CONFIG_FILE = args.size() ? args[0] : "wabbit.conf";
    if( verbose ){
        std::cout << "duration    : " << DURATION << std::endl;
        std::cout << "config_file : " << CONFIG_FILE << std::endl;
    }

    // Load the configuration file.
    bites::Config config;
    if ( not config.load(CONFIG_FILE) ){
        std::cout << "Error: Failed to load " << CONFIG_FILE << std::endl;
        usage( argv[0] );
        return 1;
    }

    /////////////////////////////////////////////////////////////////////
    //
    //  Assemble the pipeline:
    //
    //   capture -----> disk_write -----> db_write
    //   (alloc)
    //
    //  TODO: Implement resizing:
    //
    //                +---------> disk_write ---------+
    //               /                                 \
    //   capture ---+                                   +---> join ---> db_write
    //   (alloc)     \                                 / 
    //                +---> resize ---> disk_write ---+
    //
    //
    /////////////////////////////////////////////////////////////////////

    graph g;

    typedef source_node< wabbit::ImageAndTime > snode;
    snode capture( g, wabbit::Capture( config, DURATION, verbose ? &std::cout : NULL ));

    typedef function_node< wabbit::ImageAndTime, wabbit::ImageAndTime > fnode;
    int concurrency = unlimited;
    //fnode display( g, concurrency, wabbit::Display() );
    fnode diskwrite( g, concurrency, wabbit::DiskWrite( config["pics_dir"] ));
    fnode dbwrite( g, concurrency, wabbit::DBWrite( config ));

    //make_edge( capture, display );
    //make_edge( display, diskwrite );
    make_edge( capture, diskwrite );
    make_edge( diskwrite, dbwrite );
    g.wait_for_all();

    return 0;
}
