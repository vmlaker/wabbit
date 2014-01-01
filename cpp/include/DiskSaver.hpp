#ifndef WABBIT_DISKSAVER_HPP_INCLUDED
#define WABBIT_DISKSAVER_HPP_INCLUDED

// Include standard headers.
#include <vector>
#include <mutex>
#include <limits>

// Include 3rd party headers.
#include <boost/filesystem.hpp>
#include <opencv2/opencv.hpp>
#include <bites.hpp>

// Include application headers.
#include "Captor.hpp"

namespace wabbit {

/**
   Disk saving thread.
*/
class DiskSaver : public bites::Thread, 
                  protected bites::MutexedCounter<DiskSaver>
{
public:
    /**
       Initialize the disk saving thread with parameters.

       @param  root_dir      Top directory for saving the pics to.
       @param  input_queue   Input task stream.
       @param  output_queue  Output task stream.
    */
    DiskSaver(
        const boost::filesystem::path& root_dir,
        bites::ConcurrentQueue <Captor::FrameAndTime>& input_queue,
        bites::ConcurrentQueue <Captor::FrameAndTime>& output_queue
        ):
        m_root_dir (root_dir),
        m_input_queue (input_queue),
        m_output_queue (output_queue)
        {/* Empty. */}

private:
    boost::filesystem::path m_root_dir;
    bites::ConcurrentQueue <Captor::FrameAndTime>& m_input_queue;
    bites::ConcurrentQueue <Captor::FrameAndTime>& m_output_queue;

    /**
       The threaded function.
    */
    void run();
};

}  // namespace wabbit.

#endif  // WABBIT_DISKSAVER_HPP_INCLUDED
