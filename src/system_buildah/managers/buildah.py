# Copyright (C) 2017 Red Hat
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
buildah specific manager.
"""

import logging
import subprocess
import warnings

from system_buildah import util, managers

warnings.warn('The buildah manager is experimental!')


class Manager(managers.ImageManager):
    """
    Works with buildah.
    """

    def build(self, namespace, tag):
        """
        Builds a specific image.

        :param namespace: namespace passed in via cli.
        :type namespace: argparse.namespace
        :param tag: The tag to use when building.
        :type tag: str
        :raises: subprocess.CalledProcessError
        """
        logging.debug('buildah build will be used')
        command = ['buildah', 'bud', '-t', tag, '.']
        with util.pushd(namespace.path):
            subprocess.check_call(command)

    def tar(self, namespace, output):
        """
        Exports a specific image to a tar file.

        :param namespace: Namespace passed in via CLI.
        :type namespace: argparse.Namespace
        :param output: The name of the file to output.
        :type output: str
        :raises: subprocess.CalledProcessError
        """
        logging.debug('buildah tar will be used')
        logging.warn(
            'The tar result may not be usable '
            'until this manager is stablized!')
        out = self._normalize_filename(output)
        util.mkdir(out)  # Ensure the directory exists
        # NOTE: We _expand_path on out as buildah requires a full path
        full_path = util._expand_path(out)
        command = ['buildah', 'push', output, 'dir:/{}'.format(full_path)]
        # Export the layers
        subprocess.check_call(command)
        # Create a tar file from the layers
        subprocess.check_call(['tar', '-cf', '{}.tar'.format(out), out])
