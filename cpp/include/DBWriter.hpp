#ifndef WABBIT_DBWRITER_HPP_INCLUDED
#define WABBIT_DBWRITER_HPP_INCLUDED

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
   Database writer thread.
*/
class DBWriter : public bites::Thread 
{
public:
    /**
       Initialize the disk saving thread with parameters.

       @param  root_dir  Top directory for saving the pics to.
    */
    DBWriter(
        bites::Config& config,
        bites::ConcurrentQueue <Captor::FrameAndTime>& input_queue,
        bites::ConcurrentQueue <cv::Mat*>& done_queue
        ):
        m_config (config),
        m_input_queue (input_queue),
        m_done_queue (done_queue)
        {/* Empty. */}

private:
    bites::Config& m_config;
    bites::ConcurrentQueue <Captor::FrameAndTime>& m_input_queue;
    bites::ConcurrentQueue <cv::Mat*>& m_done_queue;

    /**
       The threaded function.
    */
    void run();
};

}  // namespace wabbit.

#endif  // WABBIT_DBWRITER_HPP_INCLUDED
