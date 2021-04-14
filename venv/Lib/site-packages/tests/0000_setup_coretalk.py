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

import subprocess


def setup_module(module):
    pass


def teardown_module(module):
    pass


def setup_function(function):
    pass


def teardown_function(function):
    pass


def test_install_coretalk():
    subprocess.call(['apt-get', 'install', '--yes', '--force-yes',
                     'coretalk'])


def test_enable_extension():
    if subprocess.call(['grep', 'coretalk.views.api', '/etc/corecluster/config.py']) != 0:
        subprocess.call(['sed', '-i',
                         's/LOAD_API = \[/LOAD_API = \["coretalk.views.api", \n/g',
                         '/etc/corecluster/config.py'])

    if subprocess.call(['grep', 'coretalk.models.coretalk', '/etc/corecluster/config.py']) != 0:
        subprocess.call(['sed', '-i.bak',
                         's/LOAD_MODELS = \[/LOAD_MODELS = \["coretalk.models.coretalk", \n/g',
                         '/etc/corecluster/config.py'])

def test_migate_db():
    subprocess.call(['cc-admin', 'makemigrations'])
    subprocess.call(['cc-admin', 'migrate'])


def test_restart_services():
    subprocess.call(['service', 'corecluster', 'restart'])
    subprocess.call(['service', 'uwsgi', 'restart'])
    subprocess.call(['service', 'nginx', 'restart'])
