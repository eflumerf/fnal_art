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
    cetmodules_20_migrator(".","larg4","08.12.01")

def sanitize_environments(*args):
    for env in args:
        for var in ('PATH', 'CET_PLUGIN_PATH',
                    'LD_LIBRARY_PATH', 'DYLD_LIBRARY_PATH', 'LIBRARY_PATH',
                    'CMAKE_PREFIX_PATH', 'ROOT_INCLUDE_PATH'):
            env.prune_duplicate_paths(var)
            env.deprioritize_system_paths(var)


class Larg4(CMakePackage):
    """Larg4"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/larg4"
    url      = "https://github.com/LArSoft/larg4.git"
    version('09.03.06.01', tag='v09_03_06_01', git='https://github.com/LArSoft/larg4.git', get_full_repo=True)
    version('09.03.05', tag='v09_03_05', git='https://github.com/LArSoft/larg4.git', get_full_repo=True)

    version('MVP1a', git='https://github.com/LArSoft/larg4.git', branch='feature/MVP1a')
    version('08.08.00', tag='v08_08_00', git='https://github.com/LArSoft/larg4.git', get_full_repo=True)
    version('08.08.01', tag='v08_08_01', git='https://github.com/LArSoft/larg4.git', get_full_repo=True)
    version('08.09.00', tag='v08_09_00', git='https://github.com/LArSoft/larg4.git', get_full_repo=True)
    version('08.10.00', tag='v08_10_00', git='https://github.com/LArSoft/larg4.git', get_full_repo=True)
    version('08.12.00', tag='v08_12_00', git='https://github.com/LArSoft/larg4.git', get_full_repo=True)
    version('08.12.01', tag='v08_12_01', git='https://github.com/LArSoft/larg4.git', get_full_repo=True)
    version('08.12.02', tag='v08_12_02', git='https://github.com/LArSoft/larg4.git', get_full_repo=True)

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')



    depends_on('artg4tk')
    depends_on('larevt')
    depends_on('art')
    depends_on('canvas-root-io')
    depends_on('art-root-io')
    depends_on('nug4')
    depends_on('cetmodules', type='build')

    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value)
               ]
        return args

    def setup_environment(self, spack_env, run_env):
        # Binaries.
        spack_env.prepend_path('PATH',
                               os.path.join(self.build_directory, 'bin'))
        # Ensure we can find plugin libraries.
        spack_env.prepend_path('CET_PLUGIN_PATH',
                               os.path.join(self.build_directory, 'lib'))
        run_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        # Ensure Root can find headers for autoparsing.
        for d in self.spec.traverse(root=False, cover='nodes', order='post',
                                    deptype=('link'), direction='children'):
            spack_env.prepend_path('ROOT_INCLUDE_PATH',
                                   str(self.spec[d.name].prefix.include))
            run_env.prepend_path('ROOT_INCLUDE_PATH',
                                 str(self.spec[d.name].prefix.include))
        run_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        # Perl modules.
        spack_env.prepend_path('PERL5LIB',
                               os.path.join(self.build_directory, 'perllib'))
        run_env.prepend_path('PERL5LIB', os.path.join(self.prefix, 'perllib'))
        # Set path to find fhicl files
        spack_env.prepend_path('FHICL_INCLUDE_PATH',
                               os.path.join(self.build_directory, 'job'))
        run_env.prepend_path('FHICL_INCLUDE_PATH', os.path.join(self.prefix, 'job'))
        # Set path to find gdml files
        spack_env.prepend_path('FW_SEARCH_PATH',
                               os.path.join(self.build_directory, 'job'))
        run_env.prepend_path('FW_SEARCH_PATH', os.path.join(self.prefix, 'job'))
        # Cleaup.
        sanitize_environments(spack_env, run_env)

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        # Ensure we can find plugin libraries.
        spack_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        run_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        spack_env.prepend_path('PATH', self.prefix.bin)
        run_env.prepend_path('PATH', self.prefix.bin)
        spack_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        run_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        spack_env.append_path('FHICL_FILE_PATH','{0}/job'.format(self.prefix))
        run_env.append_path('FHICL_FILE_PATH','{0}/job'.format(self.prefix))
        spack_env.append_path('FW_SEARCH_PATH','{0}/gdml'.format(self.prefix))
        run_env.append_path('FW_SEARCH_PATH','{0}/gdml'.format(self.prefix))
    version('mwm1', tag='mwm1', git='https://github.com/marcmengel/larg4.git', get_full_repo=True)
