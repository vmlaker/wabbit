// Include 3rd party headers.
#include <bites.hpp>

// Include application headers.
#include "Deallocator.hpp"

namespace wabbit {

void Deallocator::run ()
{
    // Pull from the queue while there are valid frames.
    cv::Mat* frame;
    m_input_queue.wait_and_pop (frame);
    while (frame)
    {
        delete frame;
        m_input_queue.wait_and_pop (frame);
    } 
}

}  // namespace wabbit.
