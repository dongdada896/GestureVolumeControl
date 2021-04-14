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
from pycore.utils import CloudException

api = None
cloud = None
network_pool = None

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


def test_network_pool_list():
    global api
    global network_pool
    network_pool = api.network_pool_list()
    assert(len(network_pool) > 0)


def test_network_create_out_of_pool():
    global api
    global network_pool
    #try:
    #    api.network_create(address='254.254.254.0', mask=24, name="test", mode='routed')
    #    raise Exception("network created out of pool")
    #except CloudException, e:
    #    pass


def test_network_create_in_pool():
    global api
    global network_pool
    network = api.network_create(address=network_pool[0].address, mask=25, name="test", mode='routed')
    network.delete()
