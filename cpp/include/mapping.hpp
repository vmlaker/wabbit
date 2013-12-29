#ifndef WABBIT_MAPPING_HPP_INCLUDED
#define WABBIT_MAPPING_HPP_INCLUDED

#include <string>
#include <odb/core.hxx>

namespace wabbit {

/**
   Maps the image table.
*/
#pragma db object table("images")
class Image
{
public:
    Image (const std::string& time)
        : m_time (time)
    {
    }
    
    const unsigned long id() const { return m_id; }
    const std::string& time() const { return m_time; }

private:
    friend class odb::access;

    Image () {};

    #pragma db id auto
    unsigned long m_id;

    #pragma db unique
    std::string m_time;
};

/**
   Maps the info table.
*/
#pragma db object table("info")
class Datum
{
public:
    Datum (const std::string& name, const std::string& value)
        : m_name (name),
          m_value (value)
    {
    }

    const unsigned long id() const { return m_id; }
    const std::string& name() const { return m_name; }
    const std::string& value() const { return m_value; }

private:
    friend class odb::access;

    Datum () {};

    #pragma db id auto
    unsigned long m_id;

    #pragma db unique
    std::string m_name;

    std::string m_value;
};

}  // namespace wabbit

#endif  // WABBIT_MAPPING_HPP_INCLUDED
