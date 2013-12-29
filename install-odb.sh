#!/usr/bin/env bash

############################################
#
#  Script to build ODB (ORM for C++)
#
#  Uncomment all commented-out commands 
#  for a clean download & build.
#
############################################

#rm -rf libodb
mkdir libodb
cd libodb
mkdir temp
cd temp

rm -rf libodb-2.3.0
rm -rf libodb-mysql-2.3.0
#wget http://www.codesynthesis.com/download/odb/2.3/libodb-2.3.0.tar.gz
#wget http://www.codesynthesis.com/download/odb/2.3/libodb-mysql-2.3.0.tar.gz

tar xzf libodb-2.3.0.tar.gz
cd libodb-2.3.0
./configure --prefix=`pwd`/../..
make -j8
make install
cd ..

tar xzf libodb-mysql-2.3.0.tar.gz
cd libodb-mysql-2.3.0
./configure --prefix=`pwd`/../.. --with-libodb=`pwd`/../libodb-2.3.0
make -j8
make install
cd ..

#cd ..
#rm -rf temp
