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

from pycore.models import Template
from pycore.models import VM
from pycore.models import Image
from pycore.models import Network
from pycore.models import NetworkPool
from pycore.models import Lease
import importlib


class Api():
    oc_address = None
    token = None
    debug = False

    cache = {}

    def __init__(self, address, token, debug=False):
        self.token = token
        self.oc_address = address
        self.debug = debug

        api_modules = request(self.oc_address, '/api/api/list_api_modules/', {'token': self.token}, self.debug)
        for extension in api_modules:
            extension_name = extension.split('.')[0]
            try:
                ext_model = importlib.import_module('pycore.extensions.%s.api' % extension_name)

                ext = ext_model.Api(self)
                setattr(self, extension_name, ext)
            except Exception as e:
                pass

    def get_api(self):
        if 'get_api' not in self.cache:
            self.cache['get_api'] = request(self.oc_address, 'api/api/get_list/', {'token': self.token}, self.debug)
        return self.cache

    def list_functions(self):
        if 'list_functions' not in self.cache:
            self.cache['list_functions'] = request(self.oc_address, 'api/api/list_functions/', {'token': self.token}, self.debug)
        return self.cache['list_functions']

    def list_api_modules(self):
        if 'list_api_modules' not in self.cache:
            self.cache['list_api_modules'] = request(self.oc_address, 'api/api/list_api_modules/', {'token': self.token}, self.debug)
        return self.cache['list_api_modules']

    def list_ci_modules(self):
        if 'list_ci_modules' not in self.cache:
            self.cache['list_ci_modules'] = request(self.oc_address, 'api/api/list_ci_modules/', {'token': self.token}, self.debug)
        return self.cache['list_ci_modules']

    def core_version(self):
        if 'core_version' not in self.cache:
            self.cache['core_version'] = request(self.oc_address, 'api/api/core_version/', {'token': self.token}, self.debug)
        return self.cache['core_version']

    def vm_list(self):
        '''
        List VMs
        '''
        vms = request(self.oc_address, '/api/vm/get_list/', {'token': self.token}, self.debug)
        return [VM(self.oc_address, self.token, vm, self.debug) for vm in vms]

    def vm_create(self,
                  name,
                  description,
                  template,
                  base_image):
        '''
        Create new VM
        '''
        vm = request(self.oc_address,
                     '/api/vm/create/',
                     {'token': self.token,
                      'name': name,
                      'description': description,
                      'template_id': template.id,
                      'base_image_id': base_image.id},
                     self.debug)
        return VM(self.oc_address, self.token, vm, self.debug)

    def vm_by_id(self, id):
        '''
        Get VM by id
        '''
        vm = request(self.oc_address,
                     '/api/vm/get_by_id/',
                     {'token': self.token,
                      'vm_id': id},
                     self.debug)
        return VM(self.oc_address, self.token, vm, self.debug)

    def vm_by_name(self, name):
        '''
        Get VM by name
        '''
        vms = request(self.oc_address, '/api/vm/get_list/', {'token': self.token}, self.debug)
        return [VM(self.oc_address, self.token, vm, self.debug) for vm in vms if vm['name'] == name]

    def image_list(self, type=None, access=None, prohibited_states=['deleted']):
        '''
        Get image list
        '''
        images = request(self.oc_address,
                         '/api/image/get_list/',
                         {'token': self.token,
                          'type': type,
                          'access': access,
                          'prohibited_states': prohibited_states},
                         self.debug)
        return [Image(self.oc_address, self.token, image, self.debug) for image in images]

    def image_create(self,
                     name,
                     description,
                     size,
                     image_type,
                     disk_controller='virtio',
                     access='private',
                     format='raw'):
        '''
        Create new image
        '''
        image = request(self.oc_address,
                        '/api/image/create/',
                        {'token': self.token,
                         'name': name,
                         'description': description,
                         'size': size,
                         'image_type': image_type,
                         'disk_controller': disk_controller,
                         'access': access,
                         'format': format},
                        self.debug)
        return Image(self.oc_address, self.token, image, self.debug)

    def image_by_id(self, id):
        '''
        Get image by id
        '''
        image = request(self.oc_address,
                        '/api/image/get_by_id/',
                        {'token': self.token,
                         'image_id': id},
                        self.debug)
        return Image(self.oc_address, self.token, image, self.debug)

    def image_by_name(self, name):
        images = request(self.oc_address, '/api/image/get_list/', {'token': self.token}, self.debug)
        return [Image(self.oc_address, self.token, image, self.debug) for image in images if image['name'] == name]

    def supported_disk_controllers(self):
        r = request(self.oc_address, '/api/image/get_disk_controllers/', {'token': self.token}, self.debug)
        return r

    def supported_video_devices(self):
        r = request(self.oc_address, '/api/image/get_video_devices/', {'token': self.token}, self.debug)
        return r

    def supported_network_devices(self):
        r = request(self.oc_address, '/api/image/get_network_devices/', {'token': self.token}, self.debug)
        return r

    def supported_image_types(self):
        r = request(self.oc_address, '/api/image/get_image_types/', {'token': self.token}, self.debug)
        return r

    def supported_image_formats(self):
        r = request(self.oc_address, '/api/image/get_image_formats/', {'token': self.token}, self.debug)
        return r

    def template_list(self):
        '''
        Get list of templates
        '''
        templates = request(self.oc_address, '/api/template/get_list/', {'token': self.token}, self.debug)
        return [Template(self.oc_address, self.token, template, self.debug) for template in templates]

    def template_by_id(self, id):
        '''
        Get template by id
        '''
        template = request(self.oc_address, '/api/template/get_by_id/', {'token': self.token,
                                                                         'template_id': id}, self.debug)
        return Template(self.oc_address, self.token, template, self.debug)

    def template_by_name(self, name):
        '''
        Get template by name
        '''
        templates = request(self.oc_address, '/api/template/get_list/', {'token': self.token}, self.debug)
        return [Template(self.oc_address, self.token, template, self.debug)
                for template in templates if template['name'] == name]

    def template_capabilities(self):
        caps = request(self.oc_address, '/api/template/capabilities/', {'token': self.token}, self.debug)
        return caps

    def network_create(self, mask, name, isolated=False, address=None, mode='routed'):
        '''
        Create network
        '''
        n_dict = request(self.oc_address,
                         '/api/network/create/',
                         {'token': self.token,
                          'mask': mask,
                          'name': name,
                          'address': address,
                          'isolated': isolated,
                          'mode': mode},
                         self.debug)
        return Network(self.oc_address, self.token, n_dict, self.debug)

    def network_request(self, mask, name, isolated=False, mode='routed'):
        print("Api.network_request: This method is obsolete. Use network_create")
        self.network_create(mask, name, isolated, mode)

    def network_by_id(self, id):
        '''
        Get network by id
        '''
        n_dict = request(self.oc_address,
                         '/api/network/get_by_id/',
                         {'token': self.token,
                          'network_id': id},
                         self.debug)
        return Network(self.oc_address, self.token, n_dict, self.debug)

    def network_by_name(self, name):
        '''
        Get network by name
        '''
        networks = request(self.oc_address, '/api/network/get_list/', {'token': self.token}, self.debug)
        return [Network(self.oc_address, self.token, network, self.debug)
                for network in networks if network['name'] == name]

    def network_pool_list(self):
        '''
        Get network pools
        '''
        pools = request(self.oc_address, '/api/network/get_pool_list/', {'token': self.token}, self.debug)
        return [NetworkPool(self.oc_address, self.token, n, self.debug) for n in pools]

    def network_list(self):
        '''
        List networks
        '''
        networks = request(self.oc_address, '/api/network/get_list/', {'token': self.token}, self.debug)
        return [Network(self.oc_address, self.token, network, self.debug) for network in networks]

    def lease_by_id(self, id):
        '''
        Get lease by id
        '''
        lease = request(self.oc_address, '/api/lease/get_by_id/', {'token': self.token,
                                                                   'lease_id': id}, self.debug)
        return Lease(self.oc_address, self.token, lease, self.debug)

    def lease_by_address(self, network_id, address):
        '''
        Get lease from selected by network_id network with given address
        '''
        check_version(self.oc_address, self.token, '1.3')

        leases = request(self.oc_address, '/api/lease/get_list/', {'token': self.token}, self.debug)
        for l in leases:
            if l['address'] == address and l['network_id'] == network_id:
                return Lease(self.oc_address, self.token, l, self.debug)

    def lease_list(self):
        '''
        List leases inside this network
        '''
        check_version(self.oc_address, self.token, '1.3')
        leases = request(self.oc_address, '/api/lease/get_list/', {'token': self.token}, self.debug)
        return [Lease(self.oc_address, self.token, lease, self.debug) for lease in leases]

    def storage_capabilities(self):
        check_version(self.oc_address, self.token, '15.08')
        return request(self.oc_address, '/api/storage/capabilities/', {'token': self.token}, self.debug)
