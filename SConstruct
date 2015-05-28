"""
The SCons file for Wabbit C++ codes
"""

import os

# Retrieve the debug flag, if set.
debug = bool(int(ARGUMENTS.get('debug', False)))

# Retrieve the Bites installation path.
bites_path = ARGUMENTS.get('bites', None)
if not bites_path:
    print('Please specify path to Bites installation, e.g. "bites=../bites"')
    exit(1)

###########################################
#
#  Bites
#
###########################################
# Build the Bites library (if not already done.)
SConscript(os.path.join(bites_path, 'SConstruct'))

# Assemble Bites include and library paths.
bites_inc_path = os.path.join(bites_path, 'include')
bites_lib_path = os.path.join(bites_path, 'lib')


###########################################
#
#  ODB Stuff
#
###########################################
odb_inc_path = 'libodb/include'
odb_lib_path = 'libodb/lib'
odb_exe = 'libodb/bin/odb'

# Create a custom builder for ODB compiler,
# and compile the ODB mappings into C++ sources.
action = odb_exe + ' ' + \
         '-I{} '.format(odb_inc_path) + \
         '-d mysql ' + \
         '--generate-query --generate-schema --output-dir src/cpp/odb $SOURCE'
builder = Builder(action=action) #, target='src/cpp/odb/mapping-odb.cxx')
env = Environment(BUILDERS={'ODBCompile' : builder})
odb_compile = env.ODBCompile(
    target=[
        'src/cpp/odb/mapping-odb.cxx',
        'src/cpp/odb/mapping-odb.hxx',
        'src/cpp/odb/mapping-odb.ixx',
        'src/cpp/odb/mapping.sql',
        ],
    source='src/cpp/include/mapping.hpp',
)
Default(odb_compile)

# Build the ODB mapping from the compiled C++ sources.
env = Environment(
    CPPPATH=(odb_inc_path, 'src/cpp/odb', 'src/cpp/include'),
    CXXFLAGS='-std=c++11',
) 
if debug: env.Append(CXXFLAGS=' -g')
odb_object = env.Object(target='src/cpp/odb/mapping-odb.o', source='src/cpp/odb/mapping-odb.cxx')
Default(odb_object)  # Built by default.


###########################################
#
#  C++ Executables
#
###########################################

# Build the dump program.
sources = (
    'src/cpp/src/dump.cpp',
)
libs = (
    'boost_system',
    'odb',
    'odb-mysql',
    'bites',
)
cpppath = (
    bites_inc_path, 
    'src/cpp/include',
    'libodb/include',
    'src/cpp/odb',
)
env = Environment(
    CPPPATH=cpppath,
    LIBPATH=(bites_lib_path, 'libodb/lib'),
    LIBS=libs,
    CXXFLAGS='-std=c++11',
    LINKFLAGS='-Wl,-rpath -Wl,' + odb_lib_path,
) 
if debug: env.Append(CXXFLAGS=' -g')
target = 'bin/dump'
prog = env.Program(target, sources + odb_object)
Default(prog)  # Program is built by default.

# Build the record program.
sources = (
    'src/cpp/src/record.cpp',
    'src/cpp/src/Capture.cpp',
    'src/cpp/src/DBWrite.cpp',
    'src/cpp/src/DiskWrite.cpp',
    'src/cpp/src/Display.cpp',
    'src/cpp/src/Resize.cpp',
)
libs = (
    'boost_filesystem',
    'boost_system',
    'opencv_core',
    'opencv_highgui',
    'opencv_imgproc',
    'odb',
    'odb-mysql',
    'tbb',    # Intel Threading Building Blocks
    'bites',
)
env = Environment(
    CPPPATH=(bites_inc_path, 'src/cpp/include', 'libodb/include', 'src/cpp/odb'),
    LIBPATH=(bites_lib_path, 'libodb/lib'),
    LIBS=libs,
    CXXFLAGS='-std=c++11',
    LINKFLAGS='-Wl,-rpath -Wl,' + odb_lib_path,
) 
if debug: env.Append(CXXFLAGS=' -g')
target = 'bin/record'
prog = env.Program(target, sources + odb_object)
Default(prog)  # Program is built by default.
Clean(target, 'bin')  # Delete bin/ directory upon clean.


###########################################
#
#  The Wabbit Logo
#
###########################################

SConscript('art/SConstruct')
Default('art')

copy = Builder(
    action='cp $SOURCE $TARGET',
)
env = Environment(BUILDERS={'Copy' : copy})
env.Copy(
    'doc/logo_small.png',
    'art/logo_small.png',
)
env.Copy(
    'static/logo_tiny.png',
    'art/logo_tiny.png',
)

# We're not building doc/ by default.
#Default('doc/logo_small.png')

Default('static/logo_tiny.png')
