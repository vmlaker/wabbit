#ifndef WABBIT_DISKWRITE_HPP_INCLUDED
#define WABBIT_DISKWRITE_HPP_INCLUDED

#include <string>

#include <boost/filesystem.hpp>

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
    DiskWrite( const boost::filesystem::path& root_dir, const std::string& suffix="" )
        : m_root_dir( root_dir ),
          m_suffix( suffix )
        {}

    /**
     * The function operator called by TBB.
     */
    const wabbit::ImageAndTime& operator()( const wabbit::ImageAndTime& );
    
private:
    boost::filesystem::path m_root_dir;
    std::string m_suffix;
};

}  // namespace wabbit.

#endif  // WABBIT_DISKWRITE_HPP_INCLUDED
