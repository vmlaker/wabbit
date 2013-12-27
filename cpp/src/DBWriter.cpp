// Include 3rd party headers.
#include <bites.hpp>

// Include application headers.
#include "Captor.hpp"
#include "DBWriter.hpp"

namespace wabbit {

void DBWriter::run ()
{
    // Pull from the queue while there are valid tasks.
    Captor::FrameAndTime task;
    cv::Mat* frame;
    m_input_queue.wait_and_pop(task);
    while(task.first)
    {
        // Signal done.
        m_done_queue.push (task.first);

        // Pull the next frame.
        m_input_queue.wait_and_pop (task);
    } 
}

}  // namespace wabbit.
