# -*- coding: utf-8 -*-

"""
storage.py
~~~~~~~~~~~~

This module implements settings HP OneView REST API
"""
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()

__title__ = 'storage'
__version__ = '0.0.1'
__copyright__ = '(C) Copyright (2012-2015) Hewlett Packard Enterprise ' \
                ' Development LP'
__license__ = 'MIT'
__status__ = 'Development'

###
# (C) Copyright (2012-2015) Hewlett Packard Enterprise Development LP
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
###

from hpOneView.common import *
from hpOneView.connection import *
from hpOneView.activity import *
from hpOneView.exceptions import *


class storage(object):

    def __init__(self, con):
        self._con = con
        self._activity = activity(con)

    def add_storage_system(self, host, user, passwd, blocking=True,
                           verbose=False):
        request = {'ip_hostname': host,
                   'username': user,
                   'password': passwd}
        task, body = self._con.post(uri['storage-systems'], request)
        if blocking is True:
            task = self._activity.wait4task(task, tout=600, verbose=verbose)
        return body

    def update_storage_system(self, StorageSystem, blocking=True,
                              verbose=False):
        task, body = self._con.put(StorageSystem['uri'], StorageSystem)
        if blocking is True:
            task = self._activity.wait4task(task, tout=600, verbose=verbose)
            return body
        return task

    def remove_storage_system(self, system, blocking=True, verbose=False):
        task, body = self._con.delete(system['uri'])
        if blocking is True:
            task = self._activity.wait4task(task, tout=600, verbose=verbose)
        return task

    def get_storage_systems(self):
        body = get_members(self._con.get(uri['storage-systems']))
        return body

    def get_storage_pools(self):
        body = self._con.get(uri['storage-pools'])
        return body

    def add_storage_pool(self, name, storageSystemUri, blocking=True,
                         verbose=False):
        request = {'storageSystemUri': storageSystemUri,
                   'poolName': name}
        task, body = self._con.post(uri['storage-pools'], request)
        if blocking is True:
            task = self._activity.wait4task(task, tout=600, verbose=verbose)
            if 'type' in task and task['type'].startswith('Task'):
                entity = self._activity.get_task_associated_resource(task)
                server = self._con.get(entity['resourceUri'])
                return server
        return task

    # Temporarly modify the headers passed for POST and DELTE on storage volume
    # templates in order to work around a bug. Without these headers the call
    # cause a NullPointerException on the appliance and a 400 gets returned.
    def add_storage_volume_template(self, name, capacity, shareable, storagePoolUri, state='Normal',
                                    description='', provisionType='Thin', verbose=False):
        ori_headers = self._con._headers
        self._con._headers.update({'Accept-Language': 'en'})
        self._con._headers.update({'Accept-Encoding': 'deflate'})
        template = make_storage_vol_templateV3(name,
                                               capacity,
                                               shareable,
                                               storagePoolUri,
                                               description,
                                               provisionType)

        task, body = self._con.post(uri['vol-templates'], template)
        self._con._headers = ori_headers
        return body

    # Temporarly modify the headers passed for POST and DELTE on storage volume
    # templates in order to work around a bug. Without these headers the call
    # cause a NullPointerException on the appliance and a 400 gets returned.
    def remove_storage_volume_template(self, volTemplate, blocking=True,
                                       verbose=False):
        ori_headers = self._con._headers
        self._con._headers.update({'Accept-Language': 'en'})
        task, body = self._con.delete(volTemplate['uri'])
        self._con._headers = ori_headers
        if blocking is True:
            task = self._activity.wait4task(task, tout=600, verbose=verbose)
            return body
        return task

    def get_attachable_volumes(self):
        body = self._con.get(uri['attachable-volumes'])
        return body

    # ------------------------------------
    # Storage Volume Attachments

    def get_attachments_volumes(self):
        body = self._con.get(uri['attachments'] + '?start=0&count=-1')
        return body

    def get_attachments_volumes_by_volume_uri(self, volume_uri):
        body = self._con.get(uri['attachments'] + '?filter=storageVolumeUri=' + volume_uri)
        return body

    def get_attachments_volume_repair(self):
        body = self._con.get(uri['attachments-repair'] + '?alertFixType=ExtraUnmanagedStorageVolumes')
        return body

    def get_attachments_volume_repair_by_server_uri(self, server_uri):
        body = self._con.get(uri['attachments-repair'] +
                             '?alertFixType=ExtraUnmanagedStorageVolumes' +
                             '&filter=resourceUri=' + server_uri)
        return body

    def remove_attachments_volume_repair_from_server(self, server_uri, blocking=True, verbose=False):
        request = {'type': 'ExtraUnmanagedStorageVolumes',
                   'resourceUri': server_uri}

        task, body = self._con.post(uri['attachments-repair'], request)
        if blocking is True:
            task = self._activity.wait4task(task, tout=600, verbose=verbose)
            return body
        return task

    def get_attachments_volumes_paths(self, attachment_id):
        body = self._con.get(uri['attachments'] + '/' + attachment_id + '/paths')
        return body

    def get_attachments_volumes_paths_by_id(self, attachment_id, path_id):
        body = self._con.get(uri['attachments'] + '/' + attachment_id +
                             '/paths' + '/' + path_id)
        return body

    def get_attachments_volumes_by_id(self, attachment_id):
        body = self._con.get(uri['attachments'] + '/' + attachment_id)
        return body

    # ------------------------------------

    def get_storage_volume_templates(self):
        body = self._con.get(uri['vol-templates'])
        return body

    def get_connectable_storage_volume_templates(self):
        body = self._con.get(uri['connectable-vol'])
        return body

    def add_storage_volume(self, volume, blocking=True, verbose=False):
        task, body = self._con.post(uri['storage-volumes'], volume)
        if blocking is True:
            task = self._activity.wait4task(task, tout=600, verbose=verbose)
            if 'type' in task and task['type'].startswith('Task'):
                entity = self._activity.get_task_associated_resource(task)
                volume = self._con.get(entity['resourceUri'])
                return volume
        return task

    def remove_storage_volume(self, volume, blocking=True,
                              verbose=False):
        task, body = self._con.delete(volume['uri'])
        if blocking is True:
            task = self._activity.wait4task(task, tout=600, verbose=verbose)
        return task

    def copy_storage_volume(self, vol, dest_name, blocking=True,
                            verbose=False):
        volume = make_storage_volume(dest_name,
                                     vol['provisionedCapacity'],
                                     vol['shareable'],
                                     vol['storagePoolUri'],
                                     vol['description'],
                                     vol['provisionType'])
        ret = self.add_storage_volume(volume, blocking, verbose)
        return ret

    # TODO remove the evil use/hack of the large count defaul once the
    # OneView appliance honors -1 as a valid count vaule
    def get_storage_volumes(self):
        body = self._con.get(uri['storage-volumes'] + '?start=0&count=999999')
        return body

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
