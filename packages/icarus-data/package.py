
from spack import *
import os
import glob

class IcarusData(Package):
    """Bundle of data files for icarus"""

    homepage = "https://icarus.fnal.gov/"

    version('09.28.01', sha256='42cc1b8d4a17ad7d1f1bd3e1a1446dfee953ec7109e11cf28f180ea69ca321ec',
            url="https://scisoft.fnal.gov/scisoft/packages/icarus_data/v09_26_00/icarus_data-09.26.00-noarch.tar.bz2")
    version('09.26.00', sha256 = '42cc1b8d4a17ad7d1f1bd3e1a1446dfee953ec7109e11cf28f180ea69ca321ec',
            url="https://scisoft.fnal.gov/scisoft/packages/icarus_data/v09_26_00/icarus_data-09.26.00-noarch.tar.bz2")

    def install(self, spec, prefix):
        src = glob.glob("%s/v*[0-9]" % self.stage.source_path)[0]
        install_tree(src,prefix)

    def setup_run_environment(self, env):
        env.set('ICARUS_DATA_VERSION', 'v%s' % self.version.underscored )
        env.prepend_path('WIRECELL_PATH', '%s/icarus_data/WirecellData'  % self.prefix )
        env.prepend_path('FW_SEARCH_PATH', '%s/icarus_data'  % self.prefix )
        env.prepend_path('FW_SEARCH_PATH', '%s/icarus_data/NoiseHistos'  % self.prefix )
        env.prepend_path('FW_SEARCH_PATH', '%s/icarus_data/Responses'  % self.prefix )
        env.prepend_path('FW_SEARCH_PATH', '%s/icarus_data/PhotonLibrary'  % self.prefix )
        env.prepend_path('FW_SEARCH_PATH', '%s/icarus_data/CRT'  % self.prefix )
        env.prepend_path('FW_SEARCH_PATH', '%s/icarus_data/PandoraMVAs'  % self.prefix )
        env.prepend_path('FW_SEARCH_PATH', '%s/icarus_data/database'  % self.prefix )
        env.prepend_path('CMAKE_PREFIX_PATH', '%s'  % self.prefix )
        env.prepend_path('PKG_CONFIG_PATH', '%s'  % self.prefix )

