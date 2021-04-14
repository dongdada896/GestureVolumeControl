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
userdata = None


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


def test_userdata_create():
    global api
    global userdata
    userdata = api.coretalk.userdata_create('test_user_data', 'some data')


def test_userdata_list():
    global api
    global userdata

    ud_list = api.coretalk.userdata_list()

    assert len(ud_list) >= 1
    assert ud_list[0].name == userdata.name
    assert ud_list[0].data == userdata.data


def test_userdata_edit():
    global api
    global userdata

    userdata.edit(name='another_name')
    ud_new = api.coretalk.userdata_by_id()
    assert ud_new.name == userdata.name

def test_userdata_delete():
    global userdata
    userdata.delete()
