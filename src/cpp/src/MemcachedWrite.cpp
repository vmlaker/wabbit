//  MemcachedWrite.cpp

#include <sstream>
#include <bites.hpp>
#include <date.h>
#include "MemcachedWrite.hpp"

namespace wabbit {

MemcachedWrite::MemcachedWrite( bites::Config& config,
                                std::ostream* output_stream)
  : Node( output_stream ),
    m_config( config ),
    m_memc( NULL )
{
  m_memc = memcached(config["memcached"].c_str(), config["memcached"].size());
  if(m_memc == NULL){
    vout() << "Failed to allocate." << std::endl;
  }
}
  
MemcachedWrite::MemcachedWrite( const MemcachedWrite& memcached_write )
  : Node( memcached_write ),
    m_config( memcached_write.m_config ),
    m_memc( memcached_write.m_memc )
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
  if(rc != MEMCACHED_SUCCESS){
    vout() << "Failed to set image: " << rc << " " << memcached_strerror(m_memc, rc) << std::endl;
  }
  using namespace date;
  auto tt = std::chrono::high_resolution_clock::to_time_t(image_and_time.time);
  std::stringstream ss;
  ss << image_and_time.time;
  auto sss = ss.str();

  rc = memcached_set(
    m_memc, "time", strlen("time"),
    reinterpret_cast<const char*>(sss.c_str()), sss.size(),
    0, 0
    );
  if(rc != MEMCACHED_SUCCESS){
    vout() << "Failed to set time: " << rc << " " << memcached_strerror(m_memc, rc) << std::endl;
  }

  std::string framerate;
  for( auto item : image_and_time.framerate ){
    std::stringstream ss;
    ss << item;
    framerate += std::string(ss.str()) + std::string(" ");
  }

  rc = memcached_set(
    m_memc, "framerate", strlen("framerate"),
    reinterpret_cast<const char*>(framerate.c_str()), framerate.size(),
    0, 0
    );
  if(rc != MEMCACHED_SUCCESS){
    vout() << "Failed to set framerate: " << rc << " " << memcached_strerror(m_memc, rc) << std::endl;
  }

  return image_and_time;
} 
  
}  // namespace wabbit.
