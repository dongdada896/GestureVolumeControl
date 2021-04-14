"""
Copyright (c) 2014 Maciej Nabozny

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


import settings
from pycore import Cloud
import time

api = None
cloud = None
image = None
template = None
vm = None

def setup_module(module):
    global cloud
    global api
    global template
    global image

    cloud = Cloud(settings.address, settings.login, settings.password)
    api = cloud.get_api()

    templates = api.template_list()
    template = templates[0]

    images = api.image_list()
    for img in images:
        if img.name == 'default image' and img.state == 'ok':
            image = img
            return
    raise Exception('image not found')

def teardown_module(module):
    pass

def setup_function(function):
    pass

def teardown_function(function):
    pass


def test_vm_create():
    global api
    global image
    global template
    global vm
    vm = api.vm_create('test vm', 'vm description', template, image)


def test_wait_vm_stopped():
    global api
    global vm

    for i in xrange(60):
        v = api.vm_by_id(vm.id)
        if v.state == 'stopped':
            break
        elif v.state == 'failed':
            raise Exception('vm failed')
        else:
            time.sleep(1)


def test_vm_cleanup():
    global vm
    vm.cleanup()


def test_vm_list():
    global vm
    global api

    vms = api.vm_by_name(vm.name)
    assert isinstance(vms, list)
    assert len(vms) > 0
    assert api.vm_by_id(vm.id) != None
    api.vm_list()


def test_wait_closed():
    global api
    global vm

    for i in xrange(60):
        v = api.vm_by_id(vm.id)
        if v.state == 'closed':
            return
        elif v.state == 'failed':
            raise Exception('vm failed')
        else:
            time.sleep(1)

    raise Exception('vm close timeout')
