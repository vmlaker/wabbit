/**
 *  DBWrite.cpp
 */

#include <sstream>

#include <odb/transaction.hxx>
#include <odb/mysql/database.hxx>
#include <bites.hpp>

#include "DBWrite.hpp"
#include "mapping.hpp"
#include "mapping-odb.hxx"

namespace wabbit {

DBWrite::DBWrite( bites::Config& config )
    : m_config( config ),
      m_db( m_config["username"],
            m_config["password"],
            m_config["db_name"] )
{}

DBWrite::DBWrite( const DBWrite& dbwrite )
    : m_config( dbwrite.m_config ),
      m_db( m_config["username"],
            m_config["password"],
            m_config["db_name"] )
{}

const wabbit::ImageAndTime& 
DBWrite::operator()( const wabbit::ImageAndTime& image_and_time )
{
    // Assemble the time string.
    auto tstring = bites::time2string( image_and_time.time, "%Y-%m-%d %H:%M:%S.%f" );

    // Create the image field.
    wabbit::Image img( tstring );
    
    // Start the transaction.
    odb::transaction trans( m_db.begin() );
    
    // Add the image field.
    m_db.persist( img );
    
    // Increment the size.
    typedef odb::query<wabbit::Datum> query;
    auto result = m_db.query<wabbit::Datum>( query::name == "size" );
    auto datum = result.begin();
    int size = stoi( datum->value() );
    std::stringstream ss;
    ss << size + 1;
    datum->value( ss.str() );
    m_db.update( *datum );
    
    // Update latest timestamp.
    result = m_db.query<wabbit::Datum>( query::name == "latest_tstamp" );
    datum = result.begin();
    datum->value( tstring );
    m_db.update( *datum );

    // Commit to database.
    trans.commit();

    return image_and_time;
} 

}  // namespace wabbit.
