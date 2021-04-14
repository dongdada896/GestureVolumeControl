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


# WARNING:
# Skip this test if your installation is not fresh. Executing this test on production installations may fail due to
# unknown allocation of other networks

import settings
from pycore import Cloud
import netaddr

api = None
cloud = None

def release_networks(network_list):
    for network in network_list:
        try:
            network.delete()
        except:
            pass

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


def test_allocate_after():
    """
    Allocate one network after another:
    AAAA____
    AAAABBBB
    This test assumes, that whole available network is free (unused)
    """
    global api
    network_a = api.network_create(26, "A", False)
    network_b = api.network_create(26, "B", False)

    a = netaddr.IPNetwork('%s/%s' % (network_a.address, str(network_a.mask)))
    b = netaddr.IPNetwork('%s/%s' % (network_b.address, str(network_b.mask)))
    if a.next() != b:
        raise Exception('Network is not next!')
    network_a.delete()
    network_b.delete()


def test_allocate_matching_beginning():
    """
    Allocate one network before another (C):
    AAAA____
    AAAABBBB
    ____BBBB
    CCCCBBBB
    This test assumes, that whole available network is free (unused)
    """
    global api
    network_a = api.network_create(26, "A", False)
    network_b = api.network_create(26, "B", False)

    a = netaddr.IPNetwork('%s/%s' % (network_a.address, str(network_a.mask)))
    b = netaddr.IPNetwork('%s/%s' % (network_b.address, str(network_b.mask)))
    if a.next() != b:
        release_networks([network_a, network_b])
        raise Exception('Network is not next!')
    network_a.delete()

    network_c = api.network_create(26, "C", False)
    c = netaddr.IPNetwork('%s/%s' % (network_c.address, str(network_c.mask)))
    if c != a:
        release_networks([network_c, network_b])
        raise Exception('Netowork C is not before B!')

    network_b.delete()
    network_c.delete()


def test_allocate_not_matching_begining():
    """
    This test works like previous. The only difference is that new network
    should not fit existing hole before B
    AAAA____
    AAAABBBB
    ____BBBB
    ____BBBBCCCCCCCC
    This test assumes, that whole available network is free (unused)
    """
    global api
    network_a = api.network_create(26, "A", False)
    network_b = api.network_create(26, "B", False)

    a = netaddr.IPNetwork('%s/%s' % (network_a.address, str(network_a.mask)))
    b = netaddr.IPNetwork('%s/%s' % (network_b.address, str(network_b.mask)))
    if a.next() != b:
        release_networks([network_a, network_b])
        raise Exception('Network is not next!')
    network_a.delete()

    network_c = api.network_create(25, "C", False)
    c = netaddr.IPNetwork('%s/%s' % (network_c.address, str(network_c.mask)))

    if b.next().network != c.network:
        release_networks(network_b, network_c)
        raise Exception('Netowork C is not after B!')

    network_b.delete()
    network_c.delete()


def test_allocate_matching_inside():
    """
    This test works like previous. The only difference is that new network
    should not fit existing hole before B
    AAAA________
    AAAABBBB____
    AAAABBBBCCCC
    AAAA____CCCC
    AAAADDDDCCCC
    This test assumes, that whole available network is free (unused)
    """
    global api
    network_a = api.network_create(26, "A", False)
    network_b = api.network_create(26, "B", False)
    network_c = api.network_create(26, "C", False)
    a = netaddr.IPNetwork('%s/%s' % (network_a.address, str(network_a.mask)))
    b = netaddr.IPNetwork('%s/%s' % (network_b.address, str(network_b.mask)))
    c = netaddr.IPNetwork('%s/%s' % (network_c.address, str(network_c.mask)))

    if a.next() != b:
        release_networks([network_a, network_b, network_c])
        raise Exception('B Network is not next!')
    if b.next() != c:
        release_networks([network_a, network_b, network_c])
        raise Exception('C Network is not next!')

    network_b.delete()

    network_d = api.network_create(26, "D", False)
    d = netaddr.IPNetwork('%s/%s' % (network_d.address, str(network_d.mask)))
    if d != b:
        release_networks([network_a, network_c, network_d])
        raise Exception('Network D is not in B\'s hole')

    network_a.delete()
    network_c.delete()
    network_d.delete()

def test_allocate_not_matching_inside():
    """
    This test works like previous. The only difference is that new network
    should not fit existing hole before B
    AAAA________
    AAAABBBB____
    AAAABBBBCCCC
    AAAA____CCCC
    AAAA____CCCC____DDDDDDDD
    This test assumes, that whole available network is free (unused)
    """
    global api
    network_a = api.network_create(26, "A", False)
    network_b = api.network_create(26, "B", False)
    network_c = api.network_create(26, "C", False)
    a = netaddr.IPNetwork('%s/%s' % (network_a.address, str(network_a.mask)))
    b = netaddr.IPNetwork('%s/%s' % (network_b.address, str(network_b.mask)))
    c = netaddr.IPNetwork('%s/%s' % (network_c.address, str(network_c.mask)))

    if a.next() != b:
        release_networks([network_a, network_b, network_c])
        raise Exception('B Network is not next!')
    if b.next() != c:
        release_networks([network_a, network_b, network_c])
        raise Exception('C Network is not next!')

    network_b.delete()

    network_d = api.network_create(25, "D", False)
    d = netaddr.IPNetwork('%s/%s' % (network_d.address, str(network_d.mask)))
    if c.next().next().network != d.network:
        release_networks([network_a, network_c, network_d])
        raise Exception('Network D is not after C!')

    network_a.delete()
    network_c.delete()
    network_d.delete()