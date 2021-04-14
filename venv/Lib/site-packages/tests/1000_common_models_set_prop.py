"""
Copyright (c) 2015 Maciej Nabozny

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

import os
import django

def setup_module(module):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'corecluster.settings'
    django.setup()

def teardown_module(module):
    pass

def setup_function(function):
    pass

def teardown_function(function):
    pass

def test_set_prop_cache():
    from corecluster.cache.task import Task
    t = Task()
    t.set_prop('x', 1)
    t.set_prop('y', 2)
    assert t.get_prop('x') == 1
    assert t.get_prop('y') == 2

    t.set_all_props({'a': 1, 'b': 2})
    props = t.get_all_props()
    assert 'a' in props
    assert 'b' in props
    assert 'x' not in props
    assert 'y' not in props


def test_set_prop_model():
    from corecluster.models.core.image import Image
    t = Image()
    t.set_prop('x', 1)
    t.set_prop('y', 2)
    assert t.get_prop('x') == 1
    assert t.get_prop('y') == 2

    t.set_all_props({'a': 1, 'b': 2})
    props = t.get_all_props()
    assert 'a' in props
    assert 'b' in props
    assert 'x' not in props
    assert 'y' not in props
