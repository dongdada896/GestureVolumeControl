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
from pycore import Cloud, Api
from pycore.utils import CloudException

api = None
cloud = None
token = None


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


def test_create_token():
    global token
    global cloud
    token = cloud.token_create()


def test_list_permissions():
    global cloud
    plist = cloud.permission_list()
    for p in plist:
        if p.function.startswith('api/image') or p.function.startswith('api/api'):
            p.attach(token)
    

def test_call_permited_function():
    global cloud
    global api
    global token
    api_tok = Api(cloud.oc_address, token.token)
    api_tok.image_list()


def test_call_restricted_function():
    global cloud
    global api
    global token
    api_tok = Api(cloud.oc_address, token.token)
    try:
        api_tok.vm_list()
        raise Exception('function_permited')
    except CloudException, e:
        if e.status != 'token_permission':
            raise Exception('function_failed')


def test_remove_token():
    global token
    token.delete()