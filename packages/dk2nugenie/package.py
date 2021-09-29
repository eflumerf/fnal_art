# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *

import os
import sys
libdir="%s/var/spack/repos/fnal_art/lib" % os.environ["SPACK_ROOT"]
if not libdir in sys.path:
    sys.path.append(libdir)



def patcher(x):
    cetmodules_20_migrator(".","dk2nugenie", "01.08.00")
 

class Dk2nugenie(CMakePackage):
    """This package consolidates the disparate formats of neutrino beam simulation "flux" files.
"""
    homepage = "https://cdcvs.fnal.gov/redmine/projects/dk2nu"
    url      = "https://cdcvs.fnal.gov/subversion/dk2nu/tags/v01_07_02"


    version('1.10.00',  svn="https://cdcvs.fnal.gov/subversion/dk2nu/tags/v01_10_00")
    version('01_07_02',  svn="https://cdcvs.fnal.gov/subversion/dk2nu/tags/v01_07_02")
    version('01.08.00.ub1',  svn="https://cdcvs.fnal.gov/subversion/dk2nu/tags/v01_08_00.ub1")
    version('01.08.00',  svn="https://cdcvs.fnal.gov/subversion/dk2nu/tags/v01_08_00")

    # Variant is still important even though it's not passed to compiler
    # flags (use of ROOT, etc.).
    variant('cxxstd',
            default='11',
            values=('11', '14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    depends_on('cmake', type='build')
    depends_on('root')
    depends_on('libxml2')
    depends_on('log4cpp')
    depends_on('genie')
    depends_on('dk2nudata')
    depends_on('tbb')

    parallel = False

    def patch(self):
        patch('dk2nu.patch', when='^genie@3.00.00:', working_dir='v{0}'.format(self.version))
        cmakelists=FileFilter('{0}/dk2nu/genie/CMakeLists.txt'.format(self.stage.source_path))
        cmakelists.filter('\$\{GENIE\}/src', '${GENIE}/include/GENIE')
        cmakelists.filter('\$ENV', '$')
        cmakelists.filter('execute_process', '#execute_process')

    root_cmakelists_dir = 'dk2nu'

    def cmake_args(self):
        prefix=self.prefix
        args = ['-DCMAKE_INSTALL_PREFIX=%s'%prefix,
                '-DGENIE_ONLY=ON',
                '-DTBB_LIBRARY=%s/libtbb.so'%self.spec['tbb'].prefix.lib,
                '-DGENIE_INC=%s/GENIE'%self.spec['genie'].prefix.include,
                '-DGENIE=%s'%self.spec['genie'].prefix,
                '-DGENIE_VERSION=%s'%self.spec['genie'].version,
                '-DDK2NUDATA_DIR=%s'%self.spec['dk2nudata'].prefix.lib ]

        return args

    def build(self, spec, prefix):
        with working_dir(self.build_directory, create=True):
            make('VERBOSE=t', 'all')
