#ifndef WABBIT_DEALLOCATE_HPP_INCLUDED
#define WABBIT_DEALLOCATE_HPP_INCLUDED

// Include application headers.
#include "ImageAndTime.hpp"

namespace wabbit {

/**
 *  Memory deallocation stage.
 */
class Deallocate
{
public:

    /**
     * The function operator called by TBB.
     */
    wabbit::ImageAndTime* operator()( wabbit::ImageAndTime* );
};

}  // namespace wabbit.

#endif  // WABBIT_DEALLOCATE_HPP_INCLUDED
