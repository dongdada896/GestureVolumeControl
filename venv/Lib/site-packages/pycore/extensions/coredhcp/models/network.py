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

from pycore.utils import request, check_version


class Network(object):
    parent_model = None

    def start(self, gateway_ip):
        check_version(self.parent_model.oc_address, self.parent_model.token, '16.01')
        request(self.parent_model.oc_address,
                '/api/dhcp/start/',
                {'token': self.parent_model.token,
                 'network_id': self.parent_model.id,
                 'gateway_ip': gateway_ip},
                self.parent_model.debug)

    def stop(self):
        check_version(self.parent_model.oc_address, self.parent_model.token, '16.01')
        request(self.parent_model.oc_address,
                '/api/dhcp/stop/',
                {'token': self.parent_model.token,
                 'network_id': self.parent_model.id},
                self.parent_model.debug)
