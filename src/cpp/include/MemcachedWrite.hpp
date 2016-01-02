#ifndef WABBIT_MEMCACHEDWRITE_HPP_INCLUDED
#define WABBIT_MEMCACHEDWRITE_HPP_INCLUDED

#include <libmemcached/memcached.h>
#include <bites.hpp>
#include "ImageAndTime.hpp"
#include "Node.hpp"

namespace wabbit {

//  Thread that writes to the Memcached.
class MemcachedWrite : public Node
{
public:
  //  Initialize the thread with parameters.
  //  @param  config  Application configuration object.
  MemcachedWrite( bites::Config& config,
                  std::ostream* output_stream = NULL );
  
  //  Copy-ctor needed for TBB.
  MemcachedWrite( const MemcachedWrite& );
  
  //  The function operator called by TBB.
  const wabbit::ImageAndTime& operator()( const wabbit::ImageAndTime& );
  
private:
  bites::Config& m_config;
  memcached_st* m_memc = NULL;
};

}  // namespace wabbit.

#endif  // WABBIT_MEMCACHEDWRITE_HPP_INCLUDED
