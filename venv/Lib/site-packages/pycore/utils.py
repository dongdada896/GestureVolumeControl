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

from distutils.version import StrictVersion
import requests
import hashlib
import json

request_id = 0
curl_equivalent = ''

class CloudException(Exception):
    status = ''
    description = ''

    def __init__(self, status, description=''):
        self.status = str(status)
        self.description = str(description)

    def __str__(self):
        return '%s: %s' % (self.status, self.description)

    def __unicode__(self):
        return '%s: %s' % (self.status, self.description)


class VersionException(Exception):
    pass


def request(address, function, params, debug=False):
    global request_id
    global curl_equivalent
    request_id += 1

    data = json.dumps(params)
    if debug:
        print('request (%d):\t%s( %s )' % (request_id, function, data))

    if address.endswith('/'):
        address = address[:-1]
    if function.startswith('/'):
        function = function[1:]

    curl_equivalent = curl_equivalent + 'curl -d \'' + data + '\' -H "Content-Type: application/json" -X POST ' + address + '/' + function + '\n'
    resp = requests.post(address + '/' + function, data)

    r = json.loads(resp.text)

    if debug:
        print("response (%d):\t%s" % (request_id, r['status']))
        print("\t\t" + resp.text)

    if r['status'] != 'ok':
        raise CloudException(r['status'], r['data'])
    else:
        return r['data']


def calc_hash(password, seed, method='sha512'):
    if method == 'sha512':
        return 'sha512:' + hashlib.sha512(str(password + seed).encode('utf-8')).hexdigest()
    elif method == 'sha1':
        return 'sha1:' + hashlib.sha1(str(password + seed).encode('utf-8')).hexdigest()
    elif method == 'legacy':
        return hashlib.sha1(str(password + seed).encode('utf-8')).hexdigest()
    else:
        raise CloudException('hash_not_supported')


def check_version(address, token, version):
    core_version = request(address, '/api/api/core_version/', {'token': token})
    if StrictVersion(core_version) >= StrictVersion(version):
        return core_version
    else:
        raise VersionException('version_unsupported')
