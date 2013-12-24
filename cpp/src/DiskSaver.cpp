// Include 3rd party headers.
#include <bites.hpp>

// Include application headers.
#include "DiskSaver.hpp"

namespace wabbit {

void DiskSaver::run ()
{
    // Pull from the queue while there are valid matrices.
    cv::Mat* frame;
    m_input_queue.wait_and_pop(frame);
    while(frame)
    {
        // Signal done.
        m_done_queue.push(frame);

        // Push to writer queue.
        m_writer_queue.push(frame);

        // Pull the next frame.
        m_input_queue.wait_and_pop(frame);
    } 

    // Signal database writer to stop.
    m_writer_queue.push(NULL);
}

}  // namespace wabbit.
