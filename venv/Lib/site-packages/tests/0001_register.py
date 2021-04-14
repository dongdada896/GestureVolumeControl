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

def setup_module(module):
    pass
def teardown_module(module):
    pass

def setup_function(function):
    pass

def teardown_function(function):
    pass


def test_register_user():
    cloud = Cloud.register(settings.address, settings.additional_login, settings.additional_password, settings.additional_name, settings.additional_surname, settings.additional_email, debug=True)


def test_register_additional():
    cloud = Cloud.register(settings.address, settings.login, settings.password, settings.name, settings.surname, settings.email, debug=True)


def test_api():
    cloud = Cloud(settings.address, settings.login, settings.password, debug=True)
    api = cloud.get_api()

