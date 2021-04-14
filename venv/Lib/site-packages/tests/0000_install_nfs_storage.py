"""
Copyright (c) 2014 Maciej Nabozny
              2016 Marta Nabozny
This file is part of CloudOver project.

CloudOver is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

"""
This test creates new NFS share from local disk
"""

import os
import subprocess

def setup_module(module):
    pass

def teardown_module(module):
    pass


def setup_function(function):
    pass


def teardown_function(function):
    pass


def test_install_packages():
    subprocess.call(['apt-get', 'install', '--yes', '--force-yes',
                     'nfs-kernel-server'])


def test_add_export():
    if not os.path.exists('/storage'):
        os.mkdir('/storage')

    if '/storage' not in open('/etc/exports').readall():
        f = open('/etc/exports', 'a')
        f.write('/storage *(rw,no_root_squash,no_subtree_check')
        f.close()

    subprocess.call(['chmod', '777', '/storage'])


def test_restart_services():
    subprocess.call(['service', 'nfs-kernel-server', 'restart'])