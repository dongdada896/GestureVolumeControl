"""
Copyright (c) 2015 Marta Nabozny

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
template = None
image = None


def setup_module(module):
    global cloud
    global api
    global image
    cloud = Cloud(settings.address, settings.login, settings.password, debug=True)
    api = cloud.get_api()

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

def test_fill_cluster_each_template_type():
    global api
    global image

    caps = api.template_capabilities()
    for template_id in caps.keys():
        template = api.template_by_id(template_id)
        vms = []
        for i in xrange(caps[template_id]):
            vms.append(api.vm_create('vm_%d' % i, 'capability test', template, image))

        for vm in vms:
            for i in xrange(60):
                vm_tmp = api.vm_by_id(vm.id)
                if vm_tmp.state == 'stopped':
                    break
                else:
                    time.sleep(1)

        for vm in vms:
            vm.cleanup()

        for vm in vms:
            for i in xrange(60):
                vm_tmp = api.vm_by_id(vm.id)
                if vm_tmp.state == 'closed':
                    break
                else:
                    time.sleep(1)


# def test_fill_cluster_running():
#     global api
#     global image
#
#     caps = api.template_capabilities()
#     for template_id in caps.keys():
#         template = api.template_by_id(template_id)
#         vms = []
#         for i in xrange(caps[template_id]):
#             vms.append(api.vm_create('vm_%d' % i, 'capability test', template, image))
#
#         for vm in vms:
#             for i in xrange(60):
#                 vm_tmp = api.vm_by_id(vm.id)
#                 if vm_tmp.state == 'stopped':
#                     break
#                 else:
#                     time.sleep(1)
#
#         for vm in vms:
#             vm.start()
#
#         for vm in vms:
#             for i in xrange(60):
#                 vm_tmp = api.vm_by_id(vm.id)
#                 if vm_tmp.state == 'running':
#                     break
#                 else:
#                     time.sleep(1)
#
#         for vm in vms:
#             vm.cleanup()
#
#         for vm in vms:
#             for i in xrange(60):
#                 vm_tmp = api.vm_by_id(vm.id)
#                 if vm_tmp.state == 'closed':
#                     break
#                 else:
#                     time.sleep(1)
