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
vpn = None
connection = None


def setup_module(module):
    global cloud
    global api
    global template
    global base_image
    global permanent_image
    global leases

    cloud = Cloud(settings.address, settings.login, settings.password)
    api = cloud.get_api()

    templates = api.template_list()
    template = templates[0]


    images = api.image_list()

    for img in images:
        if img.name == 'default image' and img.state == 'ok':
            base_image = img
    if base_image == None:
        raise Exception('base image not found')

    for img in images:
        if img.name == 'permanent image' and img.state == 'ok':
            permanent_image = img
    if permanent_image == None:
        raise Exception('permanent image not found')


def teardown_module(module):
    pass


def setup_function(function):
    pass


def teardown_function(function):
    pass


def test_vm_create():
    global api
    global base_image
    global permanent_image
    global template
    global vm

    vm = api.vm_create('VPN test', 'vm description', template, base_image)

def test_vpn_create():
    global api
    global vpn
    vpn = api.vpn.create('test vpn')


def test_wait_vm():
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


def test_vpn_wait():
    global api
    global vpn

    for i in xrange(60):
        vpns = api.vpn.get_list()
        for v in vpns:
            if v.id == vpn.id:
                if v.state == 'running':
                    return
                elif v.state == 'failed':
                    raise Exception('vpn failed')
                else:
                    time.sleep(1)


def test_vpn_attach():
    global vm
    global vpn

    vpn.attach(vm)


def test_vpn_detach():
    global vm
    global vpn
    global connection

    connection.detach()


def test_vm_attach_and_start():
    global vm
    global vpn

    vpn.attach(vm)
    vm.start()


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


def test_vpn_delete():
    global api
    global vpn

    vpn.delete()