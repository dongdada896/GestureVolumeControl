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

import pycore.extensions.coretalk.models.userdata
from pycore.utils import request, check_version, VersionException


class Api:
    def __init__(self, parent_model):
        # This is handler for top-level API object. It handles URL to CoreCluster's API interface
        self.parent_model = parent_model

    def userdata_by_id(self, id):
        try:
            check_version(self.parent_model.oc_address, self.parent_model.token, '15.12')
            resp = request(self.parent_model.oc_address,
                           '/api/userdata/get_by_id/',
                           {'token': self.parent_model.token, 'userdata_id': id})
        except VersionException:
            resp = request(self.parent_model.oc_address,
                           '/coreTalk/userdata/get_by_id/',
                           {'token': self.parent_model.token, 'userdata_id': id})

        return pycore.extensions.coretalk.models.userdata.UserData(self.parent_model.oc_address,
                                                                   self.parent_model.token,
                                                                   resp, self.parent_model.debug)

    def userdata_list(self):
        """
        List user data objects from cloud
        :return: list of userdata objects
        """
        try:
            check_version(self.parent_model.oc_address, self.parent_model.token, '15.12')
            resp = request(self.parent_model.oc_address, '/api/userdata/get_list/', {'token': self.parent_model.token})
        except VersionException:
            resp = request(self.parent_model.oc_address,
                           '/coreTalk/userdata/get_list/',
                           {'token': self.parent_model.token})
        return [pycore.extensions.coretalk.models.userdata.UserData(self.parent_model.oc_address,
                                                                    self.parent_model.token, ud) for ud in resp]

    def userdata_by_name(self, name):
        """
        List user data objects from cloud
        :return: list of userdata objects
        """
        try:
            check_version(self.parent_model.oc_address, self.parent_model.token, '15.12')
            resp = request(self.parent_model.oc_address,
                           '/api/userdata/get_list/',
                           {'token': self.parent_model.token})
        except VersionException:
            resp = request(self.parent_model.oc_address,
                           '/coreTalk/userdata/get_list/',
                           {'token': self.parent_model.token})
        return [pycore.extensions.coretalk.models.userdata.UserData(self.parent_model.oc_address,
                                                                    self.parent_model.token, ud)
                for ud in resp if ud['name'] == name]

    def userdata_create(self, name, data, convert_from=None):
        try:
            check_version(self.parent_model.oc_address, self.parent_model.token, '15.12')
            resp = request(self.parent_model.oc_address,
                           '/api/userdata/create/',
                           {'token': self.parent_model.token,
                            'name': name,
                            'data': data,
                            'convert_from': convert_from})
        except VersionException:
            resp = request(self.parent_model.oc_address,
                           '/coreTalk/userdata/create/',
                           {'token': self.parent_model.token,
                            'name': name,
                            'data': data})
        return pycore.extensions.coretalk.models.userdata.UserData(self.parent_model.oc_address,
                                                                   self.parent_model.token,
                                                                   resp)
