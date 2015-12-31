/**
 *  Capture.cpp
 */

#include <iomanip>
#include <stdexcept>  // std::invalid_argument

#include <bites.hpp>
#include <boost/filesystem.hpp>

#include "Capture.hpp"

namespace wabbit {

Capture::Capture( bites::Config& config,
                  const int& duration,
                  std::ostream* output_stream )
    : m_config( config ),
      m_duration( duration ),
      m_output_stream( output_stream ),
      m_video_capture(),
      m_rate_ticker({1, 5, 10})
{
    // Attempt to open device given as integer.
    // If that fails, attempt to resolve the device as a path.
    int device = -1;
    try{
        device = stod( m_config["device"] );
    }
    catch( std::invalid_argument){
        boost::filesystem::path path( m_config["device"] );

        // Resolve symbolic link.
        auto target = boost::filesystem::canonical(path).string();

        // Extract the number ABC from string /dev/videoABC
        auto length = std::string( "/dev/video" ).length();
        auto number = target.substr( length );
        device = std::stod( number );
    }
    if( m_output_stream ){
        *m_output_stream << "device: " << device << std::endl;
    }

    // Setup the OpenCV VideoCapture object.
    m_video_capture.open( device );
    if( m_output_stream ){
        *m_output_stream << "is opened: " << m_video_capture.isOpened() << std::endl;
    }
    m_video_capture.set( 3, stod( m_config["width"] ));
    m_video_capture.set( 4, stod( m_config["height"] ));

    // Compute interval needed to observe maximum FPS limit.
    float max_fps = stof( m_config["max_fps"] );
    max_fps = max_fps >= 0 ? max_fps : std::numeric_limits<float>::max();
    float interval_seconds = 1 / max_fps;
    int interval_ms = interval_seconds * 1000000;
    m_min_interval = std::chrono::microseconds( interval_ms );

    // Set the minimum read time for detecting camera disconnect.
    m_min_read = stof( m_config["min_read"] );
    
    m_prev_time = std::chrono::system_clock::now();
    m_end_time = m_prev_time + std::chrono::seconds( m_duration );
}

Capture::Capture( const Capture& capture ) 
    : m_config( capture.m_config ),
      m_duration( capture.m_duration ),
      m_output_stream( capture.m_output_stream ),
      m_video_capture( capture.m_video_capture ),
      m_rate_ticker( capture.m_rate_ticker ),
      m_prev_time( capture.m_prev_time ),
      m_end_time( capture.m_end_time ),
      m_min_interval( capture.m_min_interval ),
      m_min_read( capture.m_min_read )
{}

std::vector <float> Capture::getFramerate ()
{
    return m_framerate.get();
}

bool Capture::operator()( wabbit::ImageAndTime& image_and_time )
{
    if( !m_video_capture.isOpened() ){
        return false;
    }
    if( m_end_time <= std::chrono::system_clock::now() and m_duration >= 0 ){
        return false;
    }
    
    // Insert delay to observe maximum framerate limit.
    auto elapsed = std::chrono::system_clock::now() - m_prev_time;
    auto elapsed_ms = std::chrono::duration_cast<std::chrono::microseconds>( elapsed );
    auto sleep_ms = m_min_interval - elapsed_ms;
    sleep_ms = sleep_ms.count() < 0 ? std::chrono::microseconds(0) : sleep_ms;
    usleep( sleep_ms.count());

    // Take a snapshot.
    // The only way I could detect camera disconnect was by
    // thresholding the length of time to call read() method.
    // For some reason return value of read() is always True, 
    // even after disconnecting the camera.
    m_prev_time = std::chrono::system_clock::now();
    m_video_capture >> image_and_time.image;  // Read the image.
    elapsed = std::chrono::system_clock::now() - m_prev_time;
    image_and_time.time = m_prev_time;
    image_and_time.sequence++;
    elapsed_ms = std::chrono::duration_cast<std::chrono::microseconds>( elapsed );
    if( elapsed_ms.count()/1000000. < m_min_read )
    {
        // TODO: Write error to log instead of stdout.
        std::cout << "Error: Read time failed to meet threshold: " << std::endl;
        std::cout << std::fixed << std::setw( 10 ) << std::setprecision( 6 ) 
                  << elapsed_ms.count() / 1000000. << " (readtime) < " 
                  << m_min_read << " (threshold)" << std::endl;
        std::cout << "Probably disconnected camera." << std::endl;
        return false;
    }

    // Set the framerate.
    auto fps = m_rate_ticker.tick();
    m_framerate.set( fps );

    // Optionally print the current framerate.
    if( m_output_stream ){
        *m_output_stream << std::fixed << std::setw( 10 ) << std::setprecision( 6 ) 
                         << elapsed_ms.count()/1000000.;
        for(auto ii=begin( fps ); ii!=end( fps ); ++ii){
            *m_output_stream << std::fixed << std::setw( 7 ) << std::setprecision( 2 ) 
                             << *ii;
        }
        *m_output_stream << std::endl;
    }

    return true;
}

}  // namespace wabbit.
