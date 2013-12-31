// Include 3rd party headers.
#include <bites.hpp>
#include <boost/filesystem.hpp>

// Include application headers.
#include "Captor.hpp"
#include "DiskSaver.hpp"

namespace wabbit {

void DiskSaver::run ()
{
    // Increment the global object count.
    incrCount();

    // Pull from the queue while there are valid tasks.
    Captor::FrameAndTime task;
    m_input_queue.wait_and_pop(task);
    while(task.first)
    {
        // Assemble directory path.
        auto fpath = bites::time2dir (task.second);
        fpath = m_root_dir / fpath;

        // Create the directory.
        try
        {
            boost::filesystem::create_directories (fpath);
        }
        catch(boost::filesystem::filesystem_error)
        {
            // TODO: Handle failed directories creation.
        }

        // Assemble the image file path.
        auto fname = bites::time2string (
            task.second, 
            "__%Y-%m-%d__%H:%M:%S:%f__.jpg");
        fpath /= fname;

        // Write the image to disk.
        bool result = cv::imwrite(fpath.string(), *task.first);
        if (!result)
        {
            // TODO: Handle failed image saving.
        }

        // Signal done.
        m_done_queue.push (task.first);

        // Push to writer queue.
        m_writer_queue.push (task);

        // Pull the next frame.
        m_input_queue.wait_and_pop (task);
    } 

    if (decrCount() != 0)
    {
        // Feed input with "stop" signal.
        m_input_queue.push ({NULL, task.second});
    }
    else
    {
        // Propagate "stop" signal downstream.
        m_writer_queue.push ({NULL, task.second});
    }
}

}  // namespace wabbit.
