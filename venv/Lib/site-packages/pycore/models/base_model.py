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

from pycore.utils import request, calc_hash
import importlib


class BaseModel(object):
    api_modules = None

    def __init__(self, address, token, object_dict, debug=False):
        self.token = token
        self.oc_address = address
        self.debug = debug

        for key in object_dict.keys():
            setattr(self, key, object_dict[key])

        class_id = '%s_id' % self.__class__.__name__.lower()

        if not hasattr(self.__class__, 'api_modules'):
            self.__class__.api_modules = request(self.oc_address,
                                                 '/api/api/list_api_modules/',
                                                 {'token': self.token},
                                                 self.debug)

        if self.__class__.api_modules is None:
            self.__class__.api_modules = request(self.oc_address,
                                                 '/api/api/list_api_modules/',
                                                 {'token': self.token},
                                                 self.debug)

        self.__class__.api_modules = [m.split('.')[0] for m in self.__class__.api_modules]

        available_extensions = importlib.import_module('pycore.extensions')

        for extension in self.__class__.api_modules:
            try:
                ext_model = importlib.import_module('pycore.extensions.%s.models.%s'
                                                    % (extension, self.__class__.__name__.lower()))

                ext = getattr(ext_model, self.__class__.__name__)()
                setattr(self, extension, ext)
                setattr(ext, 'parent_model', self)
            except Exception as e:
                pass

    def __eq__(self, other):
        if other == None:
            return False
        if not isinstance(other, self.__class__):
            return False

        return self.id == other.id and self.oc_address == other.oc_address