"""The SCons file for Wabbit C++ codes."""

import os

# Retrieve the debug flag, if set.
debug = bool(int(ARGUMENTS.get('debug', False)))

# Retrieve the Bites installation path.
bites_path = ARGUMENTS.get('bites', None)
if not bites_path:
    print('Please specify path to Bites installation, e.g. "bites=../bites"')
    exit(1)

# Retrieve the Sherlock installation path.
sherlock_path = ARGUMENTS.get('sherlock', None)
if not sherlock_path:
    print('Please specify path to Sherlock C++ installation, e.g. "sherlock=../sherlock-cpp"')
    exit(1)

# Build the Sherlock library (if not already done.)
SConscript(os.path.join(sherlock_path, 'SConstruct'))

# Assemble Bites and Sherlock include and library paths.
bites_inc_path = os.path.join(bites_path, 'include')
bites_lib_path = os.path.join(bites_path, 'lib')
sherlock_inc_path = os.path.join(sherlock_path, 'include')
sherlock_lib_path = os.path.join(sherlock_path, 'lib')

# Build the record program.
sources = (
    'cpp/src/record.cpp',
    'cpp/src/Captor.cpp',
    'cpp/src/DiskSaver.cpp',
    'cpp/src/DBWriter.cpp',
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
    
    # Order is important: sherlock (1st) depends on coils (2nd).
    'sherlock',
    'bites',
)
env = Environment(
    CPPPATH=(bites_inc_path, sherlock_inc_path, 'cpp/include'),
    LIBPATH=(bites_lib_path, sherlock_lib_path),
    LIBS=libs,
    CXXFLAGS='-std=c++11',
) 
if debug: env.Append(CXXFLAGS = ' -g')
target = os.path.join('bin', 'record')
prog = env.Program(target, sources)
Default(prog)  # Program is built by default.


###########################################
#
#  ODB stuff.
#
###########################################
odb_inc_path = 'libodb/include'
odb_lib_path = 'libodb/lib'

# Custom builder for ODB compiler.
odb_compiler = Builder(
    action='odb -d mysql --generate-query --generate-schema --output-dir cpp/odb $SOURCE',
)
env = Environment(BUILDERS={'ODBCompile' : odb_compiler})
Default(env.ODBCompile('cpp/include/mapping.hpp'))
env.Clean(
    'cpp/include/mapping.hpp', (
        'cpp/odb/mapping-odb.cxx',
        'cpp/odb/mapping-odb.hxx',
        'cpp/odb/mapping-odb.ixx',
        'cpp/odb/mapping.sql',
))

# Build the ODB mapping.
libs = (
)
env = Environment(
    CPPPATH=(odb_inc_path, 'cpp/odb', 'cpp/include'),
    CXXFLAGS='-std=c++11',
) 
if debug: env.Append(CXXFLAGS = ' -g')
objects = env.Object(target = 'cpp/odb/mapping-odb.o', source = 'cpp/odb/mapping-odb.cxx')
Default(prog)  # Built by default.

# Build the dump program.
sources = (
    'cpp/src/dump.cpp',
)
libs = (
    'boost_system',
    'odb',
    'odb-mysql',
    'sherlock',
    'bites',
)
cpppath = (
    bites_inc_path, 
    sherlock_inc_path, 
    'cpp/include',
    'libodb/include',
    'cpp/odb',
)
env = Environment(
    CPPPATH=cpppath,
    LIBPATH=(bites_lib_path, sherlock_lib_path, 'libodb/lib'),
    LIBS=libs,
    CXXFLAGS='-std=c++11',
    LINKFLAGS='-Wl,-rpath -Wl,' + odb_lib_path,
) 
if debug: env.Append(CXXFLAGS = ' -g')
target = os.path.join('bin', 'dump')
prog = env.Program(target, sources + objects)
Default(prog)  # Program is built by default.
