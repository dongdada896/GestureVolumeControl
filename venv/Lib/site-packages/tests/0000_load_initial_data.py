"""
Copyright (c) 2014-2016 Maciej Nabozny
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


from django.contrib.auth.models import User
import django

import subprocess
import settings
import os
import urllib2
import uuid

def setup_module(module):
    pass


def teardown_module(module):
    pass


def setup_function(function):
    pass


def teardown_function(function):
    pass


def test_reset_db():
    if os.path.exists('/var/lib/cloudOver/overCluster.sqlite3'):
        os.remove('/var/lib/cloudOver/overCluster.sqlite3')
    subprocess.call(['cc-admin', 'makemigrations'])
    subprocess.call(['cc-admin', 'migrate'])
    subprocess.call(['chown', 'cloudover:cloudover', '/var/lib/cloudOver/overCluster.sqlite3'])


def test_setup_django():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "corecluster.settings")
    django.setup()


def test_create_admin():
    user = User.objects.create_user(settings.admin_name, 'someone@somehost.sometld', settings.admin_passwd)
    user.is_staff = True
    user.is_superuser = True
    user.save()


def test_add_small_template():
    from corecluster.models.core.template import Template
    t = Template()
    t.name = 'Small'
    t.description = 'Small template description'
    t.cpu = 1
    t.memory = 128
    t.points = 1
    t.save()


def test_add_medium_template():
    from corecluster.models.core.template import Template
    t = Template()
    t.name = 'Medium'
    t.description = 'Medium template description'
    t.cpu = 2
    t.memory = 256
    t.points = 2
    t.save()


def test_add_big_template():
    from corecluster.models.core.template import Template
    t = Template()
    t.name = 'Big'
    t.description = 'Big template description'
    t.cpu = 4
    t.memory = 1024
    t.points = 4
    t.save()


def test_add_routed_network():
    from corecluster.models.core.network_pool import NetworkPool
    t = NetworkPool()
    t.address = '10.250.0.0'
    t.mode = 'routed'
    t.access = 'public'
    t.mask = 16
    t.save()


def test_add_isolated_network():
    from corecluster.models.core.network_pool import NetworkPool
    t = NetworkPool()
    t.address = '0.0.0.0'
    t.mode = 'isolated'
    t.access = 'public'
    t.mask = 0
    t.save()


def test_add_routed_network():
    from corecluster.models.core.network_pool import NetworkPool
    t = NetworkPool()
    t.address = '192.168.0.0'
    t.mode = 'public'
    t.access = 'public'
    t.mask = 24
    t.save()


def test_add_storage():
    from corecluster.models.core.storage import Storage
    for storage in settings.storages:
        storage_url = urllib2.urlparse.urlparse(storage)
        t = Storage()
        t.name = 'storage_%s' % str(uuid.uuid4()).split('-')[0]
        t.address = storage_url.netloc
        t.dir = storage_url.path
        t.state = 'locked'
        t.transport = storage_url.scheme
        t.capacity = 10000 # 10GB, for tests
        t.save()

