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

def setup_module(module):
    global cloud
    global api
    cloud = Cloud(settings.address, settings.login, settings.password)
    api = cloud.get_api()


def teardown_module(module):
    pass


def setup_function(function):
    pass


def teardown_function(function):
    pass


def test_upload():
    global api
    global image
    image_types = api.supported_image_types()
    disk_controllers = api.supported_disk_controllers()
    image = api.image_create("upload image", "image description", 10, 'transient', disk_controllers[0], 'private', format='vdi')
    image.upload_url('http://download.cirros-cloud.net/0.3.2/cirros-0.3.2-x86_64-disk.img')


def test_wait_created():
    global api
    global image

    for i in xrange(240):
        img = api.image_by_id(image.id)
        if img.state == 'failed':
            return
        else:
            time.sleep(1)
    # raise Exception('image created with wrong format')


def test_delete():
    global api
    global image

    image.delete()
