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

# Create a custom builder for ODB compiler.
action = odb_exe + ' ' + \
         '-I{} '.format(odb_inc_path) + \
         '-d mysql ' + \
         '--generate-query --generate-schema --output-dir cpp/odb $SOURCE'
odb_compiler = Builder(action=action)
env = Environment(BUILDERS={'ODBCompile' : odb_compiler})
odb_compile = env.ODBCompile('cpp/include/mapping.hpp')
Default(odb_compile)
env.Clean(
    'cpp/include/mapping.hpp', (
        'cpp/odb/mapping-odb.cxx',
        'cpp/odb/mapping-odb.hxx',
        'cpp/odb/mapping-odb.ixx',
        'cpp/odb/mapping.sql',
))

# Build the ODB mapping.
env = Environment(
    CPPPATH=(odb_inc_path, 'cpp/odb', 'cpp/include'),
    CXXFLAGS='-std=c++11',
) 
if debug: env.Append(CXXFLAGS = ' -g')
odb_object = env.Object(target = 'cpp/odb/mapping-odb.o', source = 'cpp/odb/mapping-odb.cxx')
Default(odb_object)  # Built by default.

Depends(odb_object, odb_compile)


###########################################
#
#  C++ Executables
#
###########################################

# Build the dump program.
sources = (
    'cpp/src/dump.cpp',
)
libs = (
    'boost_system',
    'odb',
    'odb-mysql',
    'bites',
)
cpppath = (
    bites_inc_path, 
    'cpp/include',
    'libodb/include',
    'cpp/odb',
)
env = Environment(
    CPPPATH=cpppath,
    LIBPATH=(bites_lib_path, 'libodb/lib'),
    LIBS=libs,
    CXXFLAGS='-std=c++11',
    LINKFLAGS='-Wl,-rpath -Wl,' + odb_lib_path,
) 
if debug: env.Append(CXXFLAGS = ' -g')
target = os.path.join('bin', 'dump')
prog = env.Program(target, sources + odb_object)
Default(prog)  # Program is built by default.

# Build the record program.
sources = (
    'cpp/src/record.cpp',
    'cpp/src/Captor.cpp',
    'cpp/src/DiskSaver.cpp',
    'cpp/src/DBWriter.cpp',
    'cpp/src/Deallocator.cpp',
)
libs = (
    'boost_filesystem',
    'boost_thread',
    'boost_system',
    'opencv_core',
#    'opencv_contrib',
    'opencv_highgui',
#    'opencv_imgproc',
#    'opencv_objdetect',

    'odb',
    'odb-mysql',
    
    'bites',
)
env = Environment(
    CPPPATH=(bites_inc_path, 'cpp/include', 'libodb/include', 'cpp/odb'),
    LIBPATH=(bites_lib_path, 'libodb/lib'),
    LIBS=libs,
    CXXFLAGS='-std=c++11',
    LINKFLAGS='-Wl,-rpath -Wl,' + odb_lib_path,
) 
if debug: env.Append(CXXFLAGS = ' -g')
target = os.path.join('bin', 'record')
prog = env.Program(target, sources + odb_object)
Default(prog)  # Program is built by default.
