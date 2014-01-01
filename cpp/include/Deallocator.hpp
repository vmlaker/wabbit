#ifndef WABBIT_DEALLOCATOR_HPP_INCLUDED
#define WABBIT_DEALLOCATOR_HPP_INCLUDED

// Include standard headers.
#include <vector>
#include <mutex>
#include <limits>

// Include 3rd party headers.
#include <opencv2/opencv.hpp>
#include <bites.hpp>

namespace wabbit {

/**
   Deallocation thread.
*/
class Deallocator : public bites::Thread
{
public:
    /**
       Initialize the deallocator thread with parameters.

       @param  input_queue  Input stream of objects to deallocate.
    */
    Deallocator(
        bites::ConcurrentQueue <cv::Mat*>& input_queue
        ) :
        m_input_queue (input_queue)
        {/* Empty. */}

private:
    bites::ConcurrentQueue <cv::Mat*>& m_input_queue;

    /**
       The threaded function.
    */
    void run();
};

}  // namespace wabbit.

#endif  // WABBIT_DEALLOCATOR_HPP_INCLUDED
