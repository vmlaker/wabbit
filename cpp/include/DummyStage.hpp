#ifndef WABBIT_DUMMYSTAGE_HPP_INCLUDED
#define WABBIT_DUMMYSTAGE_HPP_INCLUDED

// Include standard headers.
#include <limits>

// Include 3rd party headers.
#include <bites.hpp>

// Include application headers.
#include "Captor.hpp"

namespace wabbit {

/**
   Dummy stage that does nothing.
*/
class DummyStage : public bites::Thread 
{
public:
    /**
       Initialize the dummy stage with parameters.
    */
    DummyStage(
        bites::ConcurrentQueue <cv::Mat*>& input_queue,
        bites::ConcurrentQueue <cv::Mat*>& done_queue
        ):
        m_input_queue (input_queue),
        m_done_queue (done_queue)
        {/* Empty. */}

private:
    bites::ConcurrentQueue <cv::Mat*>& m_input_queue;
    bites::ConcurrentQueue <cv::Mat*>& m_done_queue;

    /**
       The threaded function.
    */
    void run();
};

}  // namespace wabbit.

#endif  // WABBIT_DUMMYSTAGE_HPP_INCLUDED
