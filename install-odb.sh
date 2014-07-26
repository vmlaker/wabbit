#!/usr/bin/env bash

############################################
#
#  Script to build ODB (ORM for C++)
#
#  Uncomment all commented-out commands 
#  for a clean download & build.
#
############################################

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
odb_version="2.3.0"

# A clean run removes any previously worked on stuff.
if [[ $clean == 1 ]] ; then
    rm -rf odb-$odb_version
    rm -rf libodb-$odb_version
    rm -rf libodb-mysql-$odb_version
    rm -rf odb-$odb_version.tar.gz
    rm -rf libodb-$odb_version.tar.gz
    rm -rf libodb-mysql-$odb_version.tar.gz
    wget http://www.codesynthesis.com/download/odb/2.3/odb-$odb_version.tar.gz
    wget http://www.codesynthesis.com/download/odb/2.3/libodb-$odb_version.tar.gz
    wget http://www.codesynthesis.com/download/odb/2.3/libodb-mysql-$odb_version.tar.gz
    tar xzf odb-$odb_version.tar.gz
    tar xzf libodb-$odb_version.tar.gz
    tar xzf libodb-mysql-$odb_version.tar.gz
fi

# Build the ODB Compiler.
cd odb-$odb_version
./configure --prefix=`pwd`/../..
make -j $jobs
make install
cd ..

# Build the ODB Common Runtime Library.
cd libodb-$odb_version
./configure --prefix=`pwd`/../..
make -j $jobs
make install
cd ..

# Build the ODB MySQL Database Runtime Library.
cd libodb-mysql-$odb_version
./configure --prefix=`pwd`/../.. --with-libodb=`pwd`/../libodb-$odb_version
make -j $jobs
make install
cd ..

# Upon success, clean up the temporary directory.
cd ..
rm -rf temp
cd ..

# Return with a success flag.
return 0
