#ifndef WABBIT_DISPLAY_HPP_INCLUDED
#define WABBIT_DISPLAY_HPP_INCLUDED

// Include application headers.
#include "ImageAndTime.hpp"

namespace wabbit {

/*
 *  Image display.
 */
class Display
{
public:

    /*
     *  Ctor.
     */
    Display( );

    /*
     *  The function operator called by TBB.
     */
    wabbit::ImageAndTime* operator()( wabbit::ImageAndTime* );
};

}  // namespace wabbit.

#endif  // WABBIT_DISPLAY_HPP_INCLUDED
