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

imageA = None
imageB = None
test_user = None
test_taskA = None
test_taskB = None
test_taskC = None


def setup_module(module):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'corecluster.settings'
    django.setup()

def teardown_module(module):
    global test_taskA
    global test_taskB
    global test_taskC
    if test_taskA is not None:
        test_taskA.delete()
    if test_taskB is not None:
        test_taskB.delete()
    if test_taskC is not None:
        test_taskC.delete()

    test_taskA = None
    test_taskB = None
    test_taskC = None

    global test_user
    if test_user is not None:
        test_user.delete()

    global imageA
    global imageB
    if imageA is not None:
        imageA.delete()
    if imageB is not None:
        imageB.delete()

    imageA = None
    imageB = None


def setup_function(function):
    pass

def teardown_function(function):
    pass


def test_empty_queue():
    from corecluster.cache.task import Task
    global imageA
    global imageB
    imageA = None
    imageB = None

    while True:
        tasks = Task.get_task('queue_a', ['test_action'])
        if len(tasks) > 0:
            tasks[0].delete()
        else:
            break

    while True:
        tasks = Task.get_task('queue_b', ['test_action'])
        if len(tasks) > 0:
            tasks[0].delete()
        else:
            break


def test_create_user():
    global test_user

    from corecluster.models.core import User

    test_user = User.create()
    test_user.name = 'unit'
    test_user.surname = 'test'
    test_user.login = 'unittest'
    test_user.set_state('ok')


def test_create_image_objects():
    global imageA
    global imageB
    global test_user
    from corecluster.models.core import Image

    imageA = Image.create(test_user, 'imageA', 'imageA desc', 1024, 'transient', 'virtio', 'private', 'qcow2')
    imageA.save()
    imageB = Image.create(test_user, 'imageB', 'imageB desc', 1024, 'transient', 'virtio', 'private', 'qcow2')
    imageB.save()


def test_add_task():
    global imageA
    global imageB
    global test_taskA
    global test_taskB
    from corecluster.cache.task import Task

    assert imageA.last_task == None
    assert imageB.last_task == None

    test_taskA = Task()
    test_taskA.type = 'queue_a'
    test_taskA.state = 'not active'
    test_taskA.action = 'test_action'
    test_taskA.append_to([imageA, imageB])

    assert test_taskA.blockers == []

    test_taskB = Task()
    test_taskB.type = 'queue_b'
    test_taskB.state = 'not active'
    test_taskB.action = 'test_action'
    test_taskB.append_to([imageA, imageB])

    assert test_taskB.blockers == [test_taskA.cache_key(), test_taskA.cache_key()]


def test_task_check_last_task():
    global imageA
    global imageB
    global test_taskA
    global test_taskB

    from corecluster.models.core import Image

    img_a = Image.objects.get(pk=imageA.id)
    img_b = Image.objects.get(pk=imageB.id)
    assert img_a.last_task == test_taskB.cache_key()
    assert img_b.last_task == test_taskB.cache_key()


def test_get_task():
    global test_taskA
    global test_taskB

    from corecluster.cache.task import Task

    tasks = Task.get_task('queue_b', ['test_action'])

    assert len(tasks) == 0

    tasks = Task.get_task('queue_a', ['test_action'])
    assert len(tasks) > 0
    tasks[0].set_state('not active')
    tasks[0].save()
