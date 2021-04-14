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
    global vm

    cloud = Cloud(settings.address, settings.login, settings.password)
    api = cloud.get_api()

    templates = api.template_list()
    template = templates[0]

    images = api.image_list()
    for img in images:
        if img.name == 'default image' and img.state == 'ok':
            image = img
            break

    if image == None:
        raise Exception('image not found')

    vm = api.vm_create('test vm', 'vm description', template, image)

def teardown_module(module):
    pass

def setup_function(function):
    pass

def teardown_function(function):
    pass

def test_wait_vm_created():
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

def test_vm_start():
    global vm
    vm.start()

def test_wait_vm_running():
    global api
    global vm

    for i in xrange(60):
        v = api.vm_by_id(vm.id)
        if v.state == 'running':
            return
        elif v.state == 'failed':
            raise Exception('vm failed')
        else:
            time.sleep(1)

    raise Exception('vm start timeout')

def test_vm_reset():
    global vm
    vm.reset()

def test_vm_poweroff():
    global vm
    vm.poweroff()


def test_wait_vm_powered_off():
    global api
    global vm

    for i in xrange(60):
        v = api.vm_by_id(vm.id)
        if v.state == 'stopped':
            return
        elif v.state == 'failed':
            raise Exception('vm failed')
        else:
            time.sleep(1)

    raise Exception('vm poweroff timeout')

def test_vm_cleanup():
    global vm
    vm.cleanup()


def test_wait_closed():
    global api
    global vm

    for i in xrange(60):
        v = api.vm_by_id(vm.id)
        if v.state == 'closed':
            return
        elif v.state == 'failed':
            raise Exception('image failed')
        else:
            time.sleep(1)

    raise Exception('vm close timeout')