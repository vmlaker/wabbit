// Include 3rd party headers.
#include <bites.hpp>

// Include application headers.
#include "DBWriter.hpp"

namespace wabbit {

void DBWriter::run ()
{
    // Pull from the queue while there are valid matrices.
    cv::Mat* frame;
    m_input_queue.wait_and_pop(frame);
    while(frame)
    {
        // Signal done, and pull the next frame.
        m_done_queue.push(frame);
        m_input_queue.wait_and_pop(frame);
    } 
}

}  // namespace wabbit.
