"""The SCons file for Wabbit C++ codes."""

import os

# Retrieve the debug flag, if set.
debug = bool(int(ARGUMENTS.get('debug', False)))

# Build the Sherlock library.
SConscript('sherlock/SConstruct')

# Build the programs.
sources = (
    'src/cpp/record.cpp',
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
    CPPPATH=('sherlock/bites/include', 'sherlock/include'),
    LIBPATH=('sherlock/bites/lib', 'sherlock/lib'),
    LIBS=libs,
    CXXFLAGS='-std=c++11',
) 
if debug: env.Append(CXXFLAGS = ' -g')
for source in sources:
    target = source[:source.rfind('.')]
    target = os.path.basename(target)
    target = os.path.join('bin', target)
    prog = env.Program(target, source)
    Default(prog)  # Program is built by default.
