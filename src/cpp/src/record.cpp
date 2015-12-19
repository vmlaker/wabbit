//  Record video frames to disk, and mark the timestamps in database.
//
//  Parameters:  <duration_sec> [<config_file>]

#include <algorithm>
#include <csignal>
#include <sstream>
#include <string>
#include <vector>

#include <boost/filesystem.hpp>
#include <opencv2/opencv.hpp>
#include <bites.hpp>
#include "tbb/flow_graph.h"

#include "Capture.hpp"
#include "Display.hpp"
#include "DiskWrite.hpp"
#include "DBWrite.hpp"
#include "MemcachedWrite.hpp"
#include "Resize.hpp"

using namespace tbb::flow;

//  Print the usage text.
//
//  @param  argv0  Name of the command (e.g. argv[0])
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
  // Setup signal handling.
  signal(SIGTERM, [] (int value) { std::exit(value); } );
  signal(SIGINT, [] (int value) { std::exit(value); } );
  
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
  CONFIG_FILE = boost::filesystem::absolute(CONFIG_FILE).string();
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
  //  Assemble the image capture and processing pipeline.
  //
  //  The default pipeline:
  //
  //                +---> memcached_write (optional)
  //               /
  //   capture ---+---> disk_write -----> db_write
  //
  //  If resizing is enabled:
  //                
  //                +---> memcached_write (optional)
  //               /
  //   capture ---+-----------------> disk_write -----+---> join ---> funnel ---> db_write
  //               \                                 / 
  //                +---> resize ---> disk_write ---+
  //
  /////////////////////////////////////////////////////////////////////
  using namespace wabbit;
  graph g;
  typedef source_node< ImageAndTime > snode;
  snode capture( g, Capture( config, DURATION, verbose ? &std::cout : NULL ));
  typedef function_node< ImageAndTime, ImageAndTime > fnode;
  const int concurrency = unlimited;
  fnode diskwrite1( g, concurrency, DiskWrite( config["pics_dir"] ));
  fnode resize( g, concurrency, Resize( config ));
  std::string suffix( config["width2"] + "x" + config["height2"] + "__" );
  fnode diskwrite2( g, concurrency, DiskWrite( config["pics_dir"], suffix ));
  join_node< tuple< ImageAndTime, ImageAndTime > > join( g );
  function_node< tuple< ImageAndTime, ImageAndTime >, ImageAndTime > funnel(
    g, unlimited, []( const tuple< ImageAndTime, ImageAndTime > &t )
    -> const ImageAndTime& { return std::get<0>( t ); });
  fnode dbwrite( g, concurrency, DBWrite( config ));
  fnode mcdwrite( g, concurrency, MemcachedWrite( config, verbose ? &std::cout : NULL ));
  
  // Connect the flow graph.
  make_edge( capture, diskwrite1 );
  if( config["memcached"].size() ){
    make_edge( capture, mcdwrite );
  }
  if( config["width2"].empty() or config["height2"].empty() ){
    make_edge( diskwrite1, dbwrite );
  }else{
    make_edge( capture, resize );
    make_edge( resize, diskwrite2 );
    make_edge( diskwrite1, input_port<0>( join ));
    make_edge( diskwrite2, input_port<1>( join ));
    make_edge( join, funnel );
    make_edge( funnel, dbwrite );
  }
  g.wait_for_all();
  return 0;
}
