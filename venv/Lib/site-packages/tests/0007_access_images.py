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

qapi = None
mapi = None
qcloud = None
mcloud = None

def setup_module(module):
    global mcloud
    global qcloud
    global mapi
    global qapi
    mcloud = Cloud(settings.address, settings.login, settings.password)
    qcloud = Cloud(settings.address, settings.additional_login, settings.additional_password)
    mapi = mcloud.get_api()
    qapi = qcloud.get_api()

def teardown_module(module):
    pass

def setup_function(function):
    pass

def teardown_function(function):
    pass

def test_access():
    global qapi
    images = qapi.image_list()
    for image in images:
        if image.name == 'default image':
            raise Exception('transient image visible in permanent list')
        elif image.name == 'permanent image':
            raise Exception('permanent image visible in transient images')

def test_delete():
    global qapi
    global mapi
    images = mapi.image_list()
    try:
        img = qapi.image_by_id(images[0].id)
        img.delete()
    except:
        return

    raise Exception('user is permitted to delete foreign images')