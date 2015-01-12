#ifndef WABBIT_DISKWRITE_HPP_INCLUDED
#define WABBIT_DISKWRITE_HPP_INCLUDED

// Include 3rd party headers.
#include <boost/filesystem.hpp>

// Include application headers.
#include "ImageAndTime.hpp"

namespace wabbit {

/**
 *  Disk writing stage.
 */
class DiskWrite
{
public:

    /**
     *  Initialize the disk writing stage with given parameters.
     *
     *  @param  root_dir  Top directory for saving the pics to.
     */
    DiskWrite( const boost::filesystem::path& root_dir ):
        m_root_dir( root_dir ) {}

    /**
     * The function operator called by TBB.
     */
    wabbit::ImageAndTime* operator()( wabbit::ImageAndTime* );
    
private:
    boost::filesystem::path m_root_dir;
};

}  // namespace wabbit.

#endif  // WABBIT_DISKWRITE_HPP_INCLUDED
