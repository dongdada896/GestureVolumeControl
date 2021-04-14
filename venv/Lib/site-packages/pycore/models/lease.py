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


class Lease(BaseModel):
    def __str__(self):
        return self.id

    def attach(self, vm):
        """
        Attach lease to given vm
        :param vm: VM object
        """
        self.vm_id = vm.id
        request(self.oc_address, '/api/lease/attach/', {'token': self.token,
                                                        'lease_id': self.id,
                                                        'vm_id': vm.id}, self.debug)

    def detach(self):
        """
        Detach lease from vm (if attached)
        """
        request(self.oc_address, '/api/lease/detach/', {'token': self.token,
                                                        'lease_id': self.id}, self.debug)

    def redirect(self, private_lease):
        """
        Redirect this lease to another, private lease
        """
        request(self.oc_address, '/api/redirection/redirect/', {'token': self.token,
                                                                'public_lease_id': self.id,
                                                                'private_lease_id': private_lease.id})

    def remove_redirection(self, private_lease):
        """
        Redirect this lease to another, private lease
        """
        request(self.oc_address, '/api/redirection/remove_redirection/', {'token': self.token,
                                                                          'public_lease_id': self.id,
                                                                          'private_lease_id': private_lease.id})

    def enable_proxy(self, port):
        """
        Enable HTTP proxy to lease
        """
        request(self.oc_address, '/api/proxy/create/', {'token': self.token,
                                                        'lease_id': self.id,
                                                        'port': port})

    def disable_proxy(self):
        """
        Disable HTTP proxy to lease
        """
        request(self.oc_address, '/api/proxy/delete/', {'token': self.token,
                                                        'lease_id': self.id})

    def list_redirected(self):
        r = request(self.oc_address, '/api/redirection/get_list/', {'token': self.token,
                                                                    'public_lease_id': self.id})
        return [Lease(self.oc_address, self.token, l, self.debug) for l in r]
