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
from pycore.models.base_model import BaseModel


class Permission(BaseModel):
    def __init__(self, address, login, password, seed, permission_dict, debug=False):
        self.login = login
        self.password = password
        self.oc_address = address
        self.seed = seed
        self.debug = debug

        self.token = None
        tokens = request(self.oc_address, '/user/token/get_list/', {'login': self.login,
                                                                    'pw_hash': calc_hash(self.password, self.seed),
                                                                    'name': 'pycloud'}, self.debug)
        if len(tokens) == 0:
            self.token = request(self.oc_address,
                                 '/user/token/create/',
                                 {'login': self.login,
                                  'pw_hash': calc_hash(self.password, self.seed),
                                  'name': 'pycloud'},
                                 self.debug)['token']
        else:
            self.token = tokens[0]['token']

        BaseModel.__init__(self, self.oc_address, self.token, permission_dict)

    def __str__(self):
        return self.function

    def attach(self, token):
        request(self.oc_address,
                '/user/permission/attach/',
                {'login': self.login,
                 'pw_hash': calc_hash(self.password, self.seed),
                 'function': self.function,
                 'token_id': token.id})

    def detach(self, token):
        request(self.oc_address,
                '/user/permission/detach/',
                {'login': self.login,
                 'pw_hash': calc_hash(self.password, self.seed),
                 'function': self.function,
                 'token_id': token.id})
