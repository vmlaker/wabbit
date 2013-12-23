"""The SCons file for Wabbit C++ codes."""

import os

# Retrieve the debug flag, if set.
debug = bool(int(ARGUMENTS.get('debug', False)))

# Build the Sherlock library.
SConscript('sherlock/SConstruct')

# Build the programs.
sources = (
    'cpp/src/record.cpp',
    'cpp/src/DiskSaver.cpp',
)
libs = (
#    'boost_filesystem',
    'boost_thread',
    'boost_system',
    'opencv_core',
#    'opencv_contrib',
    'opencv_highgui',
#    'opencv_imgproc',
#    'opencv_objdetect',
    
    # Order is important: sherlock (1st) depends on coils (2nd).
    'sherlock',
    'bites',
)
env = Environment(
    CPPPATH=('sherlock/bites/include', 'sherlock/include', 'cpp/include'),
    LIBPATH=('sherlock/bites/lib', 'sherlock/lib'),
    LIBS=libs,
    CXXFLAGS='-std=c++11',
) 
if debug: env.Append(CXXFLAGS = ' -g')
target = os.path.join('bin', 'record')
prog = env.Program(target, sources)
Default(prog)  # Program is built by default.
