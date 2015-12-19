//  MemcachedWrite.cpp

#include <bites.hpp>
#include "MemcachedWrite.hpp"

namespace wabbit {

MemcachedWrite::MemcachedWrite( bites::Config& config,
                                std::ostream* output_stream)
  : m_config( config ),
    m_output_stream( output_stream )
{
  m_memc = memcached(config["memcached"].c_str(), config["memcached"].size());
  if( m_output_stream ){
    if(m_memc == NULL){
      *m_output_stream << "Failed to allocate." << std::endl;
    }
  }
}
  
MemcachedWrite::MemcachedWrite( const MemcachedWrite& memcached_write )
  : m_config( memcached_write.m_config ),
    m_memc( memcached_write.m_memc ),
    m_output_stream( memcached_write.m_output_stream )
{}
  
const wabbit::ImageAndTime& 
MemcachedWrite::operator()( const wabbit::ImageAndTime& image_and_time )
{
  std::vector<uchar> buf;
  cv::imencode(".jpg", image_and_time.image, buf);
  auto rc = memcached_set(
    m_memc, "image", strlen("image"), 
    reinterpret_cast<const char*>(&buf[0]), buf.size(),
    0, 0
    );
  if( m_output_stream ){
    if(rc != MEMCACHED_SUCCESS){
      *m_output_stream << "Failed to set: " << memcached_strerror(m_memc, rc) << std::endl;
    }
  }
  return image_and_time;
} 
  
}  // namespace wabbit.
