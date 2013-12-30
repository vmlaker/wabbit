// Include application headers.
#include "DummyStage.hpp"

namespace wabbit {

void DummyStage::run ()
{
    // Pull from the queue while there are valid frames.
    cv::Mat* frame;
    m_input_queue.wait_and_pop(frame);
    while(frame)
    {
        // Signal done.
        m_done_queue.push (frame);

        // Pull the next frame.
        m_input_queue.wait_and_pop (frame);
    } 
}

}  // namespace wabbit.
