#!/usr/bin/env bash

############################################
#
#  Script to build ODB (ORM for C++)
#
#  Uncomment all commented-out commands 
#  for a clean download & build.
#
############################################

# Activate for debugging purposes.
#set -x

function usage {
    echo
    echo "Usage:  $(basename $0) OPTION"
    echo
    echo "    -c | --clean      Run clean, deleting everything first"
    echo "    -j | --jobs       Number of make processes (default=1)"
    echo "    -h | --help       Print this help"
    echo
    echo "    First time invocation should use a clean run, e.g."
    echo "        $(basename $0) -c -j 4"
    echo 
    echo "    For subsequent invocations (following installation of a missing module"
    echo "    indicated in a previous attempt, for example) consider leaving out"
    echo "    the clean flag in order to prevent needless downloading of sources, e.g."
    echo "        $(basename $0) -j 8"
    echo
    exit 1
}

# Number of CPUs to use during make.
jobs=1

while [ "$1" != "" ]; do
    case $1 in
        -c | --clean )      clean=1
                            ;;
        -j | --jobs )       shift
                            jobs=$1
                            ;;
        -h | --help )       usage
                            exit
                            ;;
        * )                 usage
                            exit 1
    esac
    shift
done

# A clean run starts from scratch.
if [[ $clean == 1 ]] ; then
    rm -rf libodb
    mkdir -p libodb/temp
fi

# Will download to, and build from, a temporary directory.
cd libodb/temp

# This is the version of ODB to use.
odb_ver_major="2"
odb_ver_minor="3"
odb_ver_patch="0"
odb_ver_mm="$odb_ver_major.$odb_ver_minor"
odb_ver_full="$odb_ver_mm.$odb_ver_patch"

# This is the version of libcutl to use.
libcutl_ver_major="1"
libcutl_ver_minor="8"
libcutl_ver_patch="1"
libcutl_ver_mm="$libcutl_ver_major.$libcutl_ver_minor"
libcutl_ver_full="$libcutl_ver_mm.$odb_ver_patch"

# A clean run removes any previously worked on stuff.
if [[ $clean == 1 ]] ; then
    rm -rf odb-$odb_ver_full
    rm -rf libodb-$odb_ver_full
    rm -rf libodb-mysql-$odb_ver_full
    rm -rf libcutl-$libcutl_ver_full

    rm -rf odb-$odb_ver_full.tar.gz
    rm -rf libodb-$odb_ver_full.tar.gz
    rm -rf libodb-mysql-$odb_ver_full.tar.gz
    rm -rf libcutl-$libcutl_ver_full.tar.gz

    wget http://www.codesynthesis.com/download/odb/$odb_ver_mm/odb-$odb_ver_full.tar.gz
    wget http://www.codesynthesis.com/download/odb/$odb_ver_mm/libodb-$odb_ver_full.tar.gz
    wget http://www.codesynthesis.com/download/odb/$odb_ver_mm/libodb-mysql-$odb_ver_full.tar.gz
    wget http://www.codesynthesis.com/download/libcutl/$libcutl_ver_mm/libcutl-$libcutl_ver_full.tar.gz

    tar xzf odb-$odb_ver_full.tar.gz
    tar xzf libodb-$odb_ver_full.tar.gz
    tar xzf libodb-mysql-$odb_ver_full.tar.gz
    tar xzf libcutl-$libcutl_ver_full.tar.gz

fi

# Build the libcutl library.
cd libcutl-$libcutl_ver_full
./configure --prefix=`pwd`/../..
if [ $? -gt 0 ]; then 
    exit 
fi
make -j $jobs
make install
cd ..

# Build the ODB Common Runtime Library.
cd libodb-$odb_ver_full
./configure --prefix=`pwd`/../..
if [ $? -gt 0 ]; then 
    exit 
fi
make -j $jobs
make install
cd ..

# Build the ODB MySQL Database Runtime Library.
cd libodb-mysql-$odb_ver_full
./configure --prefix=`pwd`/../.. --with-libodb=`pwd`/../libodb-$odb_ver_full
if [ $? -gt 0 ]; then 
    exit 
fi
make -j $jobs
make install
cd ..

# Build the ODB Compiler.
cd odb-$odb_ver_full
./configure --prefix=`pwd`/../.. --with-libcutl=`pwd`/../libcutl-$libcutl_ver_full
if [ $? -gt 0 ]; then 
    exit 
fi
make -j $jobs
make install
cd ..

# Upon success, return back to the top.
cd ..
cd ..
