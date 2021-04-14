"""
Copyright 2014-2017 cloudover.io ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from pycore.utils import request
from pycore.models.base_model import BaseModel
from pycore.models.task import Task


class Image(BaseModel):
    def __init__(self, *args, **kwargs):
        super(Image, self).__init__(*args, **kwargs)
        if self.tasks is not None:
            t = []
            for task in self.tasks:
                t.append(Task(self.oc_address, self.token, task))
            self.tasks = t

    def __str__(self):
        return self.name

    def delete(self):
        request(self.oc_address, '/api/image/delete/', {'token': self.token,
                                                        'image_id': self.id}, self.debug)

    def upload_url(self, url):
        request(self.oc_address, '/api/image/upload_url/', {'token': self.token,
                                                            'image_id': self.id,
                                                            'url': url}, self.debug)

    def upload_data(self, offset, data):
        request(self.oc_address, '/api/image/upload_data/', {'token': self.token,
                                                             'image_id': self.id,
                                                             'offset': offset,
                                                             'data': data}, self.debug)

    def attach(self, vm):
        request(self.oc_address, '/api/image/attach/', {'token': self.token,
                                                        'image_id': self.id,
                                                        'vm_id': vm.id}, self.debug)

    def detach(self, vm):
        request(self.oc_address, '/api/image/detach/', {'token': self.token,
                                                        'image_id': self.id,
                                                        'vm_id': vm.id}, self.debug)

    def edit(self, **kwargs):
        for key in kwargs.keys():
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
                request(self.oc_address, '/api/image/edit/', {'token': self.token,
                                                              'image_id': self.id,
                                                               key: kwargs[key]}, self.debug)
