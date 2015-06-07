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
    echo "Usage:  $(basename $0) OPTION"
    echo 
    echo "Options:"
    echo "  -c | --clean      Run clean, deleting everything first"
    echo "  -j | --jobs       Number of make processes (default=1)"
    echo "  -h | --help       Print this help"
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

# This is the version of ODB to use.
odb_ver_major="2"
odb_ver_minor="3"
odb_ver_patch="0"
odb_ver_mm="$odb_ver_major.$odb_ver_minor"
odb_ver_full="$odb_ver_mm.$odb_ver_patch"

# A clean run starts from scratch.
if [[ $clean == 1 ]] ; then
    rm -rf libodb
fi

# Retrieve the currently installed ODB version (if any).
odb_ver_cur=`libodb/bin/odb --version 2> /dev/null | head -1 | awk '{print $NF}'`

# Based on current version (if any), decide whether to install.
if [[ $odb_ver_cur == '' ]] ; then
    echo ODB not installed, will now install.
elif [[ $odb_ver_cur != $odb_ver_full ]] ; then
    echo ODB version $odb_ver_cur installed, will now install version $odb_ver_full.
else
    echo ODB version $odb_ver_cur already installed.
    exit
fi

# Determine whether we need to apply the fix in case GCC version is >= 4.9 .
# (see http://www.codesynthesis.com/pipermail/odb-users/2014-May/001849.html)
gcc_ver=`gcc -dumpversion`
gcc_ver=`echo $gcc_ver | sed 's/\([0-9]*\.[0-9]*\).*/\1/'`
fix=`echo "$gcc_ver>=4.9" | bc`
if [[ $fix == 1 ]] ; then
    echo Detected GCC version $gcc_ver, will apply fix.
fi

# Will download to, and build from, a temporary directory.
mkdir -p libodb/temp
cd libodb/temp

# This is the version of libcutl to use.
libcutl_ver_major="1"
libcutl_ver_minor="8"
libcutl_ver_patch="1"
libcutl_ver_mm="$libcutl_ver_major.$libcutl_ver_minor"
libcutl_ver_full="$libcutl_ver_mm.$odb_ver_patch"

# Download the tarballs.
wget -nc http://www.codesynthesis.com/download/odb/$odb_ver_mm/odb-$odb_ver_full.tar.gz
wget -nc http://www.codesynthesis.com/download/odb/$odb_ver_mm/libodb-$odb_ver_full.tar.gz
wget -nc http://www.codesynthesis.com/download/odb/$odb_ver_mm/libodb-mysql-$odb_ver_full.tar.gz
wget -nc http://www.codesynthesis.com/download/libcutl/$libcutl_ver_mm/libcutl-$libcutl_ver_full.tar.gz
if [[ $fix == 1 ]] ; then
    wget -nc http://codesynthesis.com/~boris/tmp/odb/odb-$odb_ver_full-gcc-4.9.0.patch
fi
    
# Extract the tarballs.
tar --skip-old-files -xzf odb-$odb_ver_full.tar.gz
tar --skip-old-files -xzf libodb-$odb_ver_full.tar.gz
tar --skip-old-files -xzf libodb-mysql-$odb_ver_full.tar.gz
tar --skip-old-files -xzf libcutl-$libcutl_ver_full.tar.gz
        
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

#-------------------------------
# Build the ODB Compiler.
#-------------------------------

# First apply the patch to the source code.
if [[ $fix == 1 ]] ; then
    patch -p0 < odb-2.3.0-gcc-4.9.0.patch
fi

# Drop into the directory.
cd odb-$odb_ver_full

# Assemble and run the configure conmmand.
cmd="./configure --prefix=`pwd`/../.. --with-libcutl=`pwd`/../libcutl-$libcutl_ver_full"
if [[ $fix == 1 ]] ; then
    cmd="env CXXFLAGS=\"-fno-devirtualize\" $cmd"
fi
eval $cmd

if [ $? -gt 0 ]; then 
    exit 
fi
make -j $jobs
make install
cd ..

# Upon success, return back to the top.
cd ..
cd ..
