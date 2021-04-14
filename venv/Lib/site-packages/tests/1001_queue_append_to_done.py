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

    while True:
        tasks = Task.get_task('test_task', ['test_action'])
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
    from corecluster.cache.task import Task

    test_taskA = Task()
    test_taskA.type = 'test_task'
    test_taskA.state = 'not active'
    test_taskA.action = 'test_action'
    test_taskA.append_to([imageA, imageB])


def test_task_check_last_task():
    global imageA
    global imageB
    global test_taskA

    from corecluster.models.core import Image

    img_a = Image.objects.get(pk=imageA.id)
    img_b = Image.objects.get(pk=imageB.id)
    assert img_a.last_task == test_taskA.cache_key()
    assert img_b.last_task == test_taskA.cache_key()


def test_task_check_blockers():
    global test_taskA
    assert test_taskA.blockers == []


def test_get_task():
    # We have only test_taskA in queue
    global test_taskA

    from corecluster.cache.task import Task

    tasks = Task.get_task('test_task', ['test_action'])

    assert len(tasks) > 0
    assert tasks[0].cache_key() == test_taskA.cache_key()

    tasks[0].set_state('ok')
    tasks[0].save()


def test_add_second_task():
    global imageA
    global test_taskB
    from corecluster.cache.task import Task

    test_taskB = Task()
    test_taskB.type = 'test_task'
    test_taskB.state = 'not active'
    test_taskB.action = 'test_action'

    # New task is assigned only to imageA
    test_taskB.append_to([imageA])


def test_task_check_last_task_second():
    global imageA
    global imageB
    global test_taskA
    global test_taskB

    from corecluster.models.core import Image

    img_a = Image.objects.get(pk=imageA.id)
    img_b = Image.objects.get(pk=imageB.id)

    # img_a should have new taskB, img_b should have old task
    assert img_a.last_task == test_taskB.cache_key()
    assert img_b.last_task == test_taskA.cache_key()


def test_task_check_blockers_second():
    global test_taskA
    global test_taskB

    assert test_taskA.cache_key() in test_taskB.blockers
    assert len(test_taskB.blockers) == 1


def test_get_task_with_another_in_queue():
    # taskA is done, get_task should return taskB
    global test_taskB

    from corecluster.cache.task import Task

    tasks = Task.get_task('test_task', ['test_action'])

    assert len(tasks) > 0
    assert tasks[0].cache_key() == test_taskB.cache_key()

    tasks[0].set_state('ok')
    tasks[0].save()


def test_delete_tasks():
    global test_taskA
    global test_taskB

    test_taskA.delete()
    test_taskB.delete()


def test_append_third_task():
    # Append next task to empty queue
    global imageA
    global imageB
    global test_taskC

    from corecluster.cache.task import Task
    from corecluster.models.core import Image

    test_taskC = Task()
    test_taskC.type = 'test_task'
    test_taskC.state = 'not active'
    test_taskC.action = 'test_action'

    # New task is assigned only to imageA
    test_taskC.append_to([imageA])

    img_a = Image.objects.get(pk=imageA.id)

    assert img_a.last_task == test_taskC.cache_key()



def test_get_task_c():
    # Here, get_task should return only task C (A and B are removed)
    global test_taskC

    from corecluster.cache.task import Task

    tasks = Task.get_task('test_task', ['test_action'])
    assert len(tasks) > 0
    assert tasks[0].cache_key() == test_taskC.cache_key()

    tasks[0].set_state('ok')
    tasks[0].save()


def test_delete_last_task():
    test_taskC.delete()


def test_get_task_empty():
    # There is no more tasks in queue
    from corecluster.cache.task import Task

    tasks = Task.get_task('test_task', ['test_action'])
    assert len(tasks) == 0
