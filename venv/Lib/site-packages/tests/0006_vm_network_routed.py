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
network_routed = None
routed_lease = None


def setup_module(module):
    global cloud
    global api
    global template
    global image
    global network_routed

    cloud = Cloud(settings.address, settings.login, settings.password)
    api = cloud.get_api()

    templates = api.template_list()
    template = templates[0]


    images = api.image_list()
    for img in images:
        if img.name == 'default image' and img.state == 'ok':
            image = img
    if image == None:
        raise Exception('image not found')


    networks = api.network_list()
    for n in networks:
        if n.name == "Test routed network":
            network_routed = n

    if network_routed == None:
        raise Exception('network not found')


def teardown_module(module):
    pass

def setup_function(function):
    pass

def teardown_function(function):
    pass


def test_vm_create_public():
    global api
    global image
    global template
    global vm
    global network_routed
    global routed_lease


    vm = api.vm_create('Public network test', 'vm description', template, image)

    for lease in network_routed.lease_list():
        if lease.vm_id == None:
            routed_lease = lease
            lease.attach(vm)
            vm.start()
            return

    raise Exception('no lease available in routed network')


def test_wait_vm():
    global api
    global vm

    for i in xrange(120):
        v = api.vm_by_id(vm.id)
        if v.state == 'running':
            return
        elif v.state == 'failed':
            raise Exception('image failed')
        else:
            time.sleep(1)

    raise Exception('vm create timeout')


def test_vm_cleanup():
    global vm
    vm.poweroff()
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


def test_lease_detached():
    global api
    global routed_lease
    global network_routed
    lease = api.lease_by_id(routed_lease.id)
    if lease.vm_id != None:
        raise Exception('lease was not detached')