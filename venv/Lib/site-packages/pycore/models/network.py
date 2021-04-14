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

from pycore.utils import request, check_version, VersionException, CloudException
from pycore.models.lease import Lease
from pycore.models.base_model import BaseModel


class Network(BaseModel):
    def __str__(self):
        return self.id

    def delete(self):
        """
        Release network
        """
        request(self.oc_address, '/api/network/delete/', {'token': self.token,
                                                          'network_id': self.id}, self.debug)

    def release(self):
        print("Network.release: this method is obsolete. Use Network.delete")
        self.delete()

    def edit(self, **kwargs):
        for key in kwargs.keys():
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
                request(self.oc_address, '/api/network/edit/', {'token': self.token,
                                                                'network_id': self.id,
                                                                key: kwargs[key]}, self.debug)

    def allocate(self):
        """
        Allocate all leases in network
        """
        request(self.oc_address, '/api/network/allocate/', {'token': self.token,
                                                            'network_id': self.id}, self.debug)

    def lease_list(self):
        """
        List leases inside this network
        :return: List of Lease objects
        """
        check_version(self.oc_address, self.token, '1.3')
        leases = request(self.oc_address, '/api/lease/get_list/', {'token': self.token,
                                                                   'network_id': self.id}, self.debug)

        return [Lease(self.oc_address, self.token, lease, self.debug) for lease in leases]

    def lease_create(self, address):
        """
        Create new lease in network
        """
        check_version(self.oc_address, self.token, '1.3')
        l_dict = request(self.oc_address, '/api/lease/create/', {'token': self.token,
                                                                 'address': str(address),
                                                                 'network_id': self.id}, self.debug)
        return Lease(self.oc_address, self.token, l_dict, self.debug)

    def lease_get_free(self):
        """
        Get lease, which is not attached to any VM
        """
        l_dict = request(self.oc_address, '/api/lease/get_unused/', {'token': self.token,
                                                                     'network_id': self.id}, self.debug)
        return Lease(self.oc_address, self.token, l_dict, self.debug)
