// Play the image stored in Memcached.

#include <vector>
#include <libmemcached/memcached.h>
#include <opencv2/opencv.hpp>
#include <bites.hpp>

int main( int argc, char** argv )
{
  bites::Config config("wabbit.conf");
  auto memc = memcached( config["memcached"].c_str(), config["memcached"].size() );
  if( memc == NULL ){
    std::cout << "Failed to allocate." << std::endl;
    return 1;
  }
  const char* title = "Memcached image";
  cv::namedWindow( title, CV_WINDOW_NORMAL );
  while( true ){
    uint32_t flags;
    memcached_return_t rc;
    size_t value_length;
    auto value = memcached_get( memc, "image", strlen("image"), &value_length, &flags, &rc );
    std::vector<char> buffer( value, value + value_length );
    cv::Mat image = cv::imdecode( buffer, CV_LOAD_IMAGE_COLOR );
    cv::imshow( title, image ); 
    cv::waitKey( 1 );
  }
}
