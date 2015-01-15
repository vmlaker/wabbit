#ifndef WABBIT_RESIZE_HPP_INCLUDED
#define WABBIT_RESIZE_HPP_INCLUDED

#include <bites.hpp>

#include "ImageAndTime.hpp"

namespace wabbit {

/**
 *  Image resizer.
 */
class Resize
{
public:
    /**
     *  Initialize the resizer.
     *
     *  @param  config  Application configuration object.
     */
    Resize( bites::Config& config );

    /**
     *  Copy-ctor needed for TBB.
     */
    Resize( const Resize& );

    /**
     * The function operator called by TBB.
     */
    wabbit::ImageAndTime operator()( const wabbit::ImageAndTime& );

private:
    bites::Config& m_config;
};

}  // namespace wabbit.

#endif  // WABBIT_RESIZE_HPP_INCLUDED
