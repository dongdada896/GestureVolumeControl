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

import pycore.extensions.vpn.models.vpn
from pycore.utils import request, calc_hash


class Api:
    def __init__(self, parent_model):
        self.parent_model = parent_model

    def network_by_id(self, id):
        vm = request(self.oc_address,
                     '/api/vpn/get_by_id/',
                     {'token': self.token,
                      'network_id': id},
                     self.debug)
        return pycore.extensions.vpn.models.vpn.VPN(self.oc_address, self.token, vm, self.debug)

    def get_list(self):
        resp = request(self.parent_model.oc_address, '/api/vpn/get_list/', {'token': self.parent_model.token})
        return [pycore.extensions.vpn.models.vpn.VPN(self.parent_model.oc_address, self.parent_model.token, vpn)
                for vpn in resp]

    def create(self, name):
        resp = request(self.parent_model.oc_address, '/api/vpn/create/', {'token': self.parent_model.token,
                                                                          'name': name})
        return pycore.extensions.vpn.models.vpn.VPN(self.parent_model.oc_address, self.parent_model.token, resp)