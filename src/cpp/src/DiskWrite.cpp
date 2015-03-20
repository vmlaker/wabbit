/**
 *  DiskWrite.cpp
 */

#include <bites.hpp>
#include <boost/filesystem.hpp>

#include "DiskWrite.hpp"

namespace wabbit {

const wabbit::ImageAndTime& 
DiskWrite::operator()( const wabbit::ImageAndTime& image_and_time )
{
    // Assemble directory path.
    auto fpath = bites::time2dir( image_and_time.time );
    fpath = m_root_dir / fpath;

    // Create the directory.
    try
    {
        boost::filesystem::create_directories( fpath );
    }
    catch( boost::filesystem::filesystem_error )
    {
        std::cout << "fail to create dir" << std::endl;
        // TODO: Handle failed directories creation.
    }

    // Assemble the image file path.
    auto fname = bites::time2string( 
        image_and_time.time, "__%Y-%m-%d__%H:%M:%S:%f__" );
    if( m_suffix.size() ){
        fname += m_suffix;
    }
    fname += ".jpg";
    fpath /= fname;

    // Write the image to disk.
    bool result = cv::imwrite( fpath.string(), image_and_time.image );
    if( !result )
    {
        // TODO: Handle failed image saving.
    }
    return image_and_time;
}

}  // namespace wabbit.
