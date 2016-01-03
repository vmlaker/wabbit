#ifndef WABBIT_NODE_HPP_INCLUDED
#define WABBIT_NODE_HPP_INCLUDED

#include <ostream>
#include <bites.hpp>

namespace wabbit {

// Null buffer and null stream pattern
// Source: http://stackoverflow.com/a/11826666/1510289
class NullBuffer : public std::streambuf
{
public:
  NullBuffer(){};
  NullBuffer( const NullBuffer& null_buffer ){}
  int overflow( int c ){ return c; }
};
class NullStream : public std::ostream {
public: 
  NullStream() : std::ostream( &m_sb ){}
  NullStream( const NullStream& null_stream ): m_sb( null_stream.m_sb ){}
private: 
  NullBuffer m_sb;
};

// Base class for all the TBB graph nodes, containing
// some useful functionality.
class Node
{
private:
  NullStream m_null_stream;
  std::ostream* m_ostream;
public:
  Node( std::ostream* verbose_ostream = NULL )
    : m_null_stream(),
      m_ostream( verbose_ostream )
  {
    if( verbose_ostream == NULL ){
      m_ostream = &m_null_stream;
    }
  }
  Node( const Node& node )
    : m_null_stream( node.m_null_stream ),
      m_ostream( node.m_ostream ) {};

  // Returns verbose output stream.
  std::ostream& vout(){ return *m_ostream; };
};

}  // namespace wabbit.

#endif  // WABBIT_NODE_HPP_INCLUDED
