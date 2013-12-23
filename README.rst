.. image:: http://vmlaker.github.io/wabbit/logo.png
  :alt: Wabbit Logo
  :align: right
  :target: http://vmlaker.github.io/wabbit

Wabbit
======

For installation and usage see `the documentation page <http://vmlaker.github.io/wabbit>`_.

Check out the live demo at http://vmlaker.org/wabbit.

Experimental C++ build
----------------------

A C++ version of Wabbit is in the works.
You can build the codes by first downloading the complete software stack:
::

   git clone http://github.com/vmlaker/bites
   git clone http://github.com/vmlaker/sherlock-cpp
   git clone http://github.com/vmlaker/wabbit


Then build the codes:
::

   cd wabbit
   scons bites=../bites sherlock=../sherlock-cpp
