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
from pycore.extensions.vpn.models.connection import Connection


class VPN(BaseModel):
    def delete(self):
        request(self.oc_address, '/api/vpn/delete/', {'token': self.token,
                                                      'vpn_id': self.id})

    def attach(self, vm):
        connection_dict = request(self.oc_address, '/api/vpn/attach/', {'token': self.token,
                                                                        'vpn_id': self.id,
                                                                        'vm_id': vm.id})
        return Connection(self.oc_address, self.token, connection_dict)

    def client_cert(self):
        return request(self.oc_address, '/api/vpn/client_cert/', {'token': self.token,
                                                                  'vpn_id': self.id})
