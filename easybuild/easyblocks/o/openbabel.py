##
# Copyright 2013 Ghent University
#
# This file is part of EasyBuild,
# originally created by the HPC team of Ghent University (http://ugent.be/hpc/en),
# with support of Ghent University (http://ugent.be/hpc),
# the Flemish Supercomputer Centre (VSC) (https://vscentrum.be/nl/en),
# the Hercules foundation (http://www.herculesstichting.be/in_English)
# and the Department of Economy, Science and Innovation (EWI) (http://www.ewi-vlaanderen.be/en).
#
# http://github.com/hpcugent/easybuild
#
# EasyBuild is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation v2.
#
# EasyBuild is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EasyBuild.  If not, see <http://www.gnu.org/licenses/>.
##
"""
EasyBuild support for OpenBabel, implemented as an easyblock

@author: Ward Poelmans (Ghent University)
"""

import os

from easybuild.easyblocks.generic.cmakemake import CMakeMake
from easybuild.tools.modules import get_software_root
from easybuild.tools.filetools import mkdir


class EB_OpenBabel(CMakeMake):
    """Support for installing the OpenBabel package."""

    def configure_step(self):
        try:
            self.openbabelbuilddir = os.path.join(self.builddir, 'EasyBuild')
            mkdir(self.openbabelbuilddir)
            os.chdir(self.openbabelbuilddir)
        except OSError, err:
            self.log.error("Failed to create build dir(%s): %s" % (self.openbabelbuilddir, err))

        self.cfg['configopts'] += " -DPYTHON_BINDINGS=ON "
        self.cfg['configopts'] += "-DENABLE_TESTS=ON "
        # Needs wxWidgets
        self.cfg['configopts'] += "-DBUILD_GUI=OFF "

        root_eigen = get_software_root("Eigen")
        if root_eigen:
            self.log.info("Using Eigen")
            self.cfg['configopts'] += "-DEIGEN3_INCLUDE_DIR='%s/include' " % root_eigen
        else:
            self.log.info("Not using Eigen")

        super(EB_OpenBabel, self).configure_step(srcdir=self.cfg['start_dir'])

    def make_module_extra(self):
        """Custom variables for OpenBabel module."""
        txt = super(EB_OpenBabel, self).make_module_extra()
        txt += self.moduleGenerator.set_environment('PYTHONPATH', '$root/lib')
        txt += self.moduleGenerator.set_environment('BABEL_LIBDIR', '$root/lib/openbabel/%s/' % self.version)
        txt += self.moduleGenerator.set_environment('BABEL_DATADIR', '$root/share/openbabel/%s/' % self.version)
        return txt
