#ifndef WABBIT_DBWRITE_HPP_INCLUDED
#define WABBIT_DBWRITE_HPP_INCLUDED

// Include 3rd party headers.
#include <bites.hpp>
#include <odb/mysql/database.hxx>

// Include application headers.
#include "ImageAndTime.hpp"

namespace wabbit {

/*
 *  Database write thread.
 */
class DBWrite
{
public:

    /*
     *  Initialize the disk saving thread with parameters.
     *
     *  @param  config  Application configuration object.
     */
    DBWrite( bites::Config& config );

    /**
     *  Copy-ctor needed for TBB.
     */
    DBWrite( const DBWrite& );

    /**
     * The function operator called by TBB.
     */
    wabbit::ImageAndTime* operator()( wabbit::ImageAndTime* );
    
private:
    bites::Config& m_config;
    odb::mysql::database m_db;
};

}  // namespace wabbit.

#endif  // WABBIT_DBWRITE_HPP_INCLUDED
