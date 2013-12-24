#ifndef __DBWRITER_HPP__
#define __DBWRITER_HPP__

// Include standard headers.
#include <vector>
#include <mutex>
#include <limits>

// Include 3rd party headers.
#include <boost/filesystem.hpp>
#include <opencv2/opencv.hpp>
#include <bites.hpp>

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

#endif  // __DBWRITER_HPP__
