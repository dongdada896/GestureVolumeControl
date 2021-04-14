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

import math
import settings
from pycore import Cloud
from pycore.utils import CloudException

api = None
cloud = None

def setup_module(module):
    global cloud
    global api
    cloud = Cloud(settings.address, settings.login, settings.password, debug=True)
    api = cloud.get_api()

def teardown_module(module):
    pass

def setup_function(function):
    pass

def teardown_function(function):
    pass


def test_routed_lease_in_quota():
    global cloud

    quota = cloud.account_quota()
    mask = int(32 - math.floor(math.log(int(quota['routed_lease_quota']) * 4, 2)) )
    net = api.network_create(name='in', mask=mask, mode='routed')
    net.delete()


def test_routed_lease_over_quota():
    global cloud

    quota = cloud.account_quota()
    try:
        mask = int(32 - math.floor(math.log(int(quota['routed_lease_quota']) * 4, 2)) - 1)
        net = api.network_create(name='in', mask=mask, mode='routed')
        net.delete()
    except:
        return
    raise Exception('network over quota allowed')


def test_public_lease_in_quota():
    global cloud

    quota = cloud.account_quota()
    mask = int(32 - math.floor(math.log(int(quota['public_lease_quota']), 2)))
    net = api.network_create(name='in', mask=mask, mode='public')
    net.delete()


def test_routed_public_over_quota():
    global cloud

    quota = cloud.account_quota()
    try:
        mask = int(32 - math.floor(math.log(int(quota['public_lease_quota']), 2)) - 1)
        net = api.network_create(name='in', mask=mask, mode='public')
        net.delete()
    except:
        return
    raise Exception('network over quota allowed')


def test_isolated_network_quota():
    global cloud

    networks = []
    quota = cloud.account_quota()
    for i in xrange(int(quota['isolated_network_quota'])):
        networks.append(api.network_create(name='isolated%d' % i, mask=24, mode='isolated', address='10.0.0.0'))

    try:
        api.network_create(name='isolated%d' % i, mask=24, mode='isolated', address='10.0.0.0')
        raise Exception('done')
    except CloudException:
        pass
    except:
        raise Exception('isolated network over quota allowed')

    for net in networks:
        net.delete()


def routed_lease_over_quota():
    global cloud

    quota = cloud.account_quota()
    try:
        mask = int(32 - math.floor(math.log(int(quota['routed_lease_quota']), 2)))
        net = api.network_create(name='in', mask=mask, mode='routed')
        net.delete()
    except:
        return
    raise Exception('network over quota allowed')