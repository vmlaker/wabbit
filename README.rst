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

That's right, a C++ version of Wabbit is in the works!

The code uses `ODB <http://www.codesynthesis.com/products/odb>`_,
a very nice object-relational mapping implementation for C++. 
Wabbit uses ODB to access the MySQL database backend.
In order to install ODB, you will first need C++ bindings for MySQL.
If you're on a system equipped with Aptitude package manager,
you can easily get the bindings via:
::

   aptitude install libmysql++-dev

Next, get the Wabbit codes:
::

   git clone http://github.com/vmlaker/bites
   git clone http://github.com/vmlaker/sherlock-cpp
   git clone http://github.com/vmlaker/wabbit
   cd wabbit

Now you're ready to install ODB and the remainder of the Wabbit software stack:
::

   sh install-odb.sh
   scons bites=../bites sherlock=../sherlock-cpp
