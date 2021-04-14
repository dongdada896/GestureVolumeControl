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

api = None
cloud = None

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

def test_account():
    global cloud
    cloud.token_list()


def test_capabilities():
    global api
    api.supported_disk_controllers()
    api.supported_network_devices()
    api.supported_video_devices()
    api.supported_image_types()

def test_listings():
    global api
    api.template_list()
    api.image_list()
    api.vm_list()
