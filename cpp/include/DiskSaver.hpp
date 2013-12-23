#ifndef __DISKSAVER_HPP__
#define __DISKSAVER_HPP__

// Include standard headers.
#include <vector>
#include <mutex>
#include <limits>

// Include 3rd party headers.
#include <boost/filesystem.hpp>
#include <opencv2/opencv.hpp>
#include <bites.hpp>

namespace sherlock {

/**
   Video capture thread.
*/
class DiskSaver : public bites::Thread 
{
public:
    /**
       Initialize the disk saving thread with parameters.

       @param  root_dir  Top directory for saving the pics to.
    */
    DiskSaver(
        const boost::filesystem::path& root_dir,
        bites::ConcurrentQueue <cv::Mat*>& input_queue,
        bites::ConcurrentQueue <cv::Mat*>& done_queue
        ):
        m_root_dir (root_dir),
        m_input_queue (input_queue),
        m_done_queue (done_queue)
        {/* Empty. */}

private:
    boost::filesystem::path m_root_dir;
    bites::ConcurrentQueue <cv::Mat*>& m_input_queue;
    bites::ConcurrentQueue <cv::Mat*>& m_done_queue;

    /**
       The threaded function.
    */
    void run();
};

}  // namespace sherlock.

#endif  // __DISKSAVER_HPP__
