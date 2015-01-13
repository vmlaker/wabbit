// Include standard headers.
#include <iomanip>

// Include 3rd party headers.
#include <bites.hpp>

// Include application headers.
#include "Capture.hpp"
#include <unistd.h>

namespace wabbit {

Capture::Capture( bites::Config& config,
                  const int& duration,
                  std::ostream* output_stream )
    : m_config( config ),
      m_duration( duration ),
      m_output_stream( output_stream ),
      m_video_capture( atoi( m_config["device"].c_str())),
      m_rate_ticker({1, 5, 10})
{
    m_video_capture.set( 3, atoi(m_config["width"].c_str()) );
    m_video_capture.set( 4, atoi(m_config["height"].c_str() ));

    // Compute interval needed to observe maximum FPS limit.
    float max_fps = atof( m_config["max_fps"].c_str());
    max_fps = max_fps >= 0 ? max_fps : std::numeric_limits<float>::max();
    float interval_seconds = 1 / max_fps;
    int interval_ms = interval_seconds * 1000000;
    m_min_interval = std::chrono::microseconds( interval_ms );

    // Set the minimum read time for detecting camera disconnect.
    m_min_read = atof( m_config["min_read"].c_str() );
    
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
