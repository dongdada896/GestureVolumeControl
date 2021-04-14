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
network = None

def setup_module(module):
    global mcloud
    global qcloud
    global mapi
    global qapi
    global network
    mcloud = Cloud(settings.address, settings.login, settings.password)
    qcloud = Cloud(settings.address, settings.additional_login, settings.additional_password)
    mapi = mcloud.get_api()
    qapi = qcloud.get_api()
    network = qapi.network_create(26, 'Q', False)

def teardown_module(module):
    global network
    network.delete()

def setup_function(function):
    pass

def teardown_function(function):
    pass

def test_get():
    global network
    global mapi
    try:
        mapi.network_by_id(network.id)
    except:
        return

    raise Exception('Network is accessible for other accounts')
