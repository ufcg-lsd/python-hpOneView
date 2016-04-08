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

from hpOneView.activity import *

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


class storage(object):

    def __init__(self, con):
        self._con = con
        self._activity = activity(con)

    ###########################################################################
    # Storage System: represents a storage disk array like HP 3PAR StoreServ Storage.
    # The storage system APIs enables bringing a storage disk array under the management of appliance.
    ###########################################################################

    def get_storage_systems(self, filter=''):
        """Gets information about all managed storage systems.

         The storage system attributes can be used with filtering and sorting operation: name, model, serialNumber,
         firmware, status, managedDomain, and state.

         Examples:
            1 - Gets all storage systems (default)

                filter = ?start=0&count=-1

            2 - Gets maximum of 5 storage systems which belong to model of type myExampleModel,
            sorted by freeCapacity in descending order.

                filter = ?start=0&count=5&sort=freeCapacity:desc&filter="model='myExampleModel'"

        :param filter: string with optional parameters to apply filtering and sorting operation
        """
        url = make_url(uri['storage-systems'], filter=filter)

        body = get_members(self._con.get(url))
        return body

    def add_storage_system(self, host, user, password, blocking=True, verbose=False):
        """Adds a storage system for management by the appliance.

        The storage system resource created will be in a "Connected" state and will not yet be available for further
        operations. Users are required to perform a PUT API on the storage system resource to complete the management of
        the storage system resource. An asynchronous task will be created as a result of this API call to discover
        available domains, target ports, and storage pools.

        :param host: IP address or host name of the storage system
        :param user: password for the specified user
        :param password: user name for the storage system

        :param blocking:
        :param verbose:
        """
        request = {'ip_hostname': host, 'username': user, 'password': password}

        task, body = self._con.post(uri['storage-systems'], request)
        if blocking is True:
            task = self._activity.wait4task(task, tout=600, verbose=verbose)
        return body

    def get_storage_systems_host_types(self):
        body = self._con.get(uri['host-types'])
        return body

    def get_storage_pools_in_storage_system(self, sto_system_id, filter=''):
        """Gets a list of Storage pools.

        Returns a list of storage pools belonging to the storage system referred by the Path property {StorageSystemId}
        parameters. Filters are supported for the following storage pool attributes only - name, domain, deviceSpeed,
        deviceType, supprtedRAIDLevel, status and state.

        :param sto_system_id: ID of Storage System
        :param filter: string with optional parameters to apply filtering and sorting operation
        """
        url = make_url(uri['storage-systems'], sto_system_id, 'storage-pools', filter=filter)

        body = get_members(self._con.get(url))
        return body

    def get_storage_system_by_id(self, sto_system_id):
        """Gets the specified storage system resource.

        :param sto_system_id: ID of specific storage system
        """
        url = make_url(uri['storage-systems'], sto_system_id)

        body = self._con.get(url)
        return body

    def update_storage_system(self, sto_system, force=False, blocking=True, verbose=False):
        """Updates the storage system.

        This API can be used to update storage system credentials, storage system attributes or to request a
        refresh of storage system.

        For updating credentials, users are allowed to update IP/hostname, username, and password.

        To request a refresh of a storage system user must set the "refreshState" attribute to RefreshPending state.

        :param sto_system: the storage system that will be updating.
        :param force: if set to true the operation completes despite any problems with network connectivity or errors on
        the resource itself. The default is false.

        :param blocking:
        :param verbose:

        """
        url = make_url(sto_system['uri'], force=force)

        task, body = self._con.put(url, sto_system)
        if blocking is True:
            task = self._activity.wait4task(task, tout=600, verbose=verbose)
            return body
        return task

    def remove_storage_system(self, sto_system_id, force=False, blocking=True, verbose=False):
        """Removes the storage system from OneView.

        :param sto_system_id: ID of storage system that will be removed from OneView.
        :param force: if set to true the operation completes despite any problems with network connectivity or errors on
        the resource itself. The default is false.

        :param blocking:
        :param verbose:
        """
        url = make_url(uri['storage-systems'], sto_system_id, force=force)

        task, body = self._con.delete(url)
        if blocking is True:
            task = self._activity.wait4task(task, tout=600, verbose=verbose)
        return task

    def get_storage_system_managed_ports(self, sto_system_id, filter=''):
        """Gets all managed target ports for the specified storage system.

         Examples:
            1 - Gets all managed ports belonging to storage system (default)

                filter = ?start=0&count=-1

            2 - Get maximum of 5 managed target ports belonging to storage system with id 123-45-67-89-123 that are in
            Normal state and sorted by portName in ascending order

                filter = ?start=0&count=5&sort=portName:asc&filter=state='Normal'

            3 - Get maximum of 3 managed target ports belonging to storage system with id 123-45-67-89-123 which belongs
            to network /rest/fc-networks/123-45-67 and sorted by portName in ascending order and belongs

                filter = ?start=0&count=3&sort=portName:asc&query="expectedNetworkUri EQ '/rest/fc-networks/123-45-67'"

        :param sto_system_id: ID of storage system that will be target to get all managed ports
        :param filter: string with optional parameters to apply filtering and sorting operation
        """
        url = make_url(uri['storage-systems'], sto_system_id, 'managedPorts', filter=filter)

        body = get_members(self._con.get(url))
        return body

    def get_storage_system_managed_port_by_port_id(self, sto_system_id, port_id):
        url = make_url(uri['storage-systems'], sto_system_id, 'managedPorts', port_id)

        body = self._con.get(url)
        return body

    ###########################################################################
    # Storage Pool: resource represents logical space on storage system from where the volumes can be carved out.
    ###########################################################################

    def get_storage_pools(self, filter=''):
        """Gets a list of storage pools.

        Returns a list of storage pools based on optional sorting and filtering, and constrained by start and count
        parameters. The storage pool attributes can be used with filtering and sorting operation:
        name, domain, deviceType, deviceSpeed, supportedRAIDLevel, status and state.

        Examples:
            1 - Gets all storage pools (default)

                filter = ?start=0&count=-1

            2 - Get maximum of 5 storage pools which has name myName and sorted by free capacity in descending order

                filter = ?start=0&count=5&sort=freeCapacity:desc&filter="name='myName'"

        :param filter: string with optional parameters to apply filtering and sorting operation
        """
        url = make_url(uri['storage-pools'], filter=filter)

        body = get_members(self._con.get(url))
        return body

    def add_storage_pool(self, name, sto_system_uri, blocking=True, verbose=False):
        """Adds storage pool for management by the appliance.

        :param name: name of storage pool to be imported
        :param sto_system_uri: URI of the storage system associated with this pool

        :param blocking:
        :param verbose:
        """
        request = {'storageSystemUri': sto_system_uri, 'poolName': name}

        task, body = self._con.post(uri['storage-pools'], request)
        if blocking is True:
            task = self._activity.wait4task(task, tout=600, verbose=verbose)
            if 'type' in task and task['type'].startswith('Task'):
                entity = self._activity.get_task_associated_resource(task)
                server = self._con.get(entity['resourceUri'])
                return server
        return task

    def get_storage_pool_by_id(self, sto_pool_id):
        """Gets the storage pool resource for the specified ID.

        :param sto_pool_id: ID of specific storage pool
        """
        url = make_url(uri['storage-pools'], sto_pool_id)

        body = self._con.get(url)
        return body

    def remove_storage_pool(self, sto_pool_id, force=False, blocking=True, verbose=False):
        """Removes an imported storage pool from OneView

        :param sto_pool_id: ID of specific storage pool that will be removed
        :param force: if set to true the operation completes despite any problems with network connectivity or errors on
        the resource itself. The default is false

        :param blocking:
        :param verbose
        """
        url = make_url(uri['storage-pools'], sto_pool_id, force=force)

        task, body = self._con.delete(url)
        if blocking is True:
            task = self._activity.wait4task(task, tout=600, verbose=verbose)
            return body
        return task

    ###########################################################################
    # Storage Volume Attachments: resource represents the connection information for the volume.
    ###########################################################################

    def get_attachments_volumes(self, filter=''):
        """Gets a list of volume attachment resources.

        Examples:
            1 - Gets all storage volume attachments (default)

                filter = ?start=0&count=-1

            2 - Get all storage volume attachments filtering by storage volume URI

                filter = ?filter=storageVolumeUri='{storageVolumeURI}'

        :param filter: string with optional parameters to apply filtering and sorting operation
        """
        url = make_url(uri['attachments'], filter=filter)

        body = get_members(self._con.get(url))
        return body

    def get_attachments_volumes_repair(self, alert_fix_type='ExtraUnmanagedStorageVolumes', filter=''):
        """Gets the list of extra unmanaged storage volumes.

        Examples:
            1 - Get the list of extra unmanaged storage volumes for the specified
            resourceUri='/rest/server-profiles/123-45-67-89-124'

                filter = ?filter="resourceUri='/rest/server-profiles/123-45-67-89-124'"

        :param alert_fix_type: type of alert fix of extra unmanaged storage volumes
        :param filter: string with optional parameters to apply filtering and sorting operation
        """
        if filter:
            filter += '&alertFixType=' + alert_fix_type
        else:
            filter += '?alertFixType=' + alert_fix_type

        url = make_url(uri['attachments-repair'], filter=filter)

        body = get_members(self._con.get(url))
        return body

    def remove_attachments_volumes_repair_from_server(self, server_uri, alert_fix_type='ExtraUnmanagedStorageVolumes',
                                                      blocking=True, verbose=False):
        """Removes extra presentations from a specified server profile.

        :param server_uri: URI of specific server profile that will be removed extra presentations
        :param alert_fix_type: type of alert fix of extra unmanaged storage volumes

        :param blocking:
        :param verbose:
        """
        request = {'type': alert_fix_type, 'resourceUri': server_uri}

        task, body = self._con.post(uri['attachments-repair'], request)
        if blocking is True:
            task = self._activity.wait4task(task, tout=600, verbose=verbose)
            return body
        return task

    def get_attachments_volumes_paths(self, attachment_id):
        """Gets all volume attachment paths.

        :param attachment_id: ID of specific volume attachment
        """
        url = make_url(uri['attachments'], attachment_id, 'paths')

        body = self._con.get(url)
        return body

    def get_attachments_volumes_paths_by_id(self, attachment_id, path_id):
        """Gets a volume attachment path by id.

        :param attachment_id: ID of specific volume attachment
        :param path_id: ID of specific path in volume attachment
        """
        url = make_url(uri['attachments'], attachment_id, 'paths', path_id)

        body = self._con.get(url)
        return body

    def get_attachments_volumes_by_id(self, attachment_id):
        """Gets a volume attachment by id.

        :param attachment_id: ID of specific volume attachment
        """
        url = make_url(uri['attachments'], attachment_id)

        body = self._con.get(url)
        return body

    ###########################################################################
    # Storage Volume Templates: resource models a set of parameters to use for volume creation.
    ###########################################################################

    def get_storage_volume_templates(self, filter=''):
        """Gets a list of storage volume templates.

        Examples:
            1 - Get all storage volume templates (default)

                filter = ?start=0&count=-1

            2 - Get storage volume template filtering by name

                filter = ?filter=name='MyTemplate'

        :param filter: string with optional parameters to apply filtering and sorting operation
        """
        url = make_url(uri['vol-templates'], filter=filter)

        body = get_members(self._con.get(url))
        return body

    def add_storage_volume_template(self, name, capacity, sto_pool_uri, shareable, provision_type, description='',
                                    sto_system_uri=None, snapshot_pool_uri=None, blocking=True, verbose=False):
        """Creates a new storage volume template.

        :param name: name for the storage volume template resource
        :param capacity: capacity requested for the volume in GiB
        :param sto_pool_uri: URI of storage pool from which the volume to be created
        :param shareable: describes if the volume is shareable (public) or private
        :param provision_type: provisioning type of the volume - Thin or Full
        :param description: description of the storage volume template resource
        :param sto_system_uri: URI of storage system which contains the storage volume template
        :param snapshot_pool_uri: URI of storage pool from which the snapshots to be created

        :param blocking
        :param verbose:
        """
        request = make_storage_volume_template_v3(name, capacity, sto_pool_uri, shareable, provision_type,
                                                  description, sto_system_uri, snapshot_pool_uri)

        # Temporally modify the headers passed for POST and DELETE on storage volume
        # templates in order to work around a bug. Without these headers the call
        # cause a NullPointerException on the appliance and a 400 gets returned.
        ori_headers = self._con._headers
        self._con._headers.update({'Accept-Language': 'en'})
        self._con._headers.update({'Accept-Encoding': 'deflate'})

        task, body = self._con.post(uri['vol-templates'], request)
        self._con._headers = ori_headers
        if blocking is True:
            task = self._activity.wait4task(task, tout=600, verbose=verbose)
            return body
        return task

    def get_connectable_storage_volume_templates(self, filter=''):
        """Gets the storage volume templates that are available on the specified networks based on the storage system
        port's expected network connectivity.

        Examples:
            1 - Get all the storage volume templates which are accessible over
            /rest/fc-networks/123-45-67 and /rest/fc-networks/111-222-333 network

                filter = ?query='availableNetworks IN [/rest/fc-networks/123-45-67,/rest/fc-networks/111-222-333]'

        :param filter: string with optional parameters to apply filtering and sorting operation
        """
        url = make_url(uri['connectable-vol'], filter=filter)

        body = self._con.get(url)
        return body

    def get_storage_volume_template_by_id(self, template_id):
        """Gets the storage volume template for the specified URI.

        :param template_id: ID of specific storage volume template
        """
        url = make_url(uri['vol-templates'], template_id)

        body = self._con.get(url)
        return body

    def update_storage_volume_template(self, template, force=False, blocking=True, verbose=False):
        """Updates a storage volume template.

        :param template: the storage volume template that will be updating
        :param force: if set to true the operation completes despite any problems with network connectivity or errors on
        the resource itself. The default is false

        :param blocking:
        :param verbose:
        """
        url = make_url(template['uri'], force=force)

        task, body = self._con.put(url, template)
        if blocking is True:
            task = self._activity.wait4task(task, tout=600, verbose=verbose)
            return body
        return task

    def remove_storage_volume_template(self, template_id, force=False, blocking=True, verbose=False):
        """Deletes the specified storage volume template.

        :param template_id: ID of specific storage volume template that will be removed
        :param force: if set to true the operation completes despite any problems with network connectivity or errors on
        the resource itself. The default is false

        :param blocking:
        :param verbose:
        """
        url = make_url(uri['vol-templates'], template_id, force=force)

        # Temporally modify the headers passed for POST and DELETE on storage volume
        # templates in order to work around a bug. Without these headers the call
        # cause a NullPointerException on the appliance and a 400 gets returned.
        ori_headers = self._con._headers
        self._con._headers.update({'Accept-Language': 'en'})
        self._con._headers.update({'Accept-Encoding': 'deflate'})

        task, body = self._con.delete(url)
        self._con._headers = ori_headers
        if blocking is True:
            task = self._activity.wait4task(task, tout=600, verbose=verbose)
            return body
        return task

    ###########################################################################
    # Volumes: represents logical space on the storage system.
    ###########################################################################

    def get_storage_volumes(self, filter=''):
        """Gets a list of all managed volumes.

        Filters are supported for the following volume attributes only - name, provisionType, state, and status.

        Examples:
            1 - Get all volumes managed by the appliance (default)

                filter = ?start=0&count=-1

            2 - Get maximum of 5 volumes which are 'Thin' provisioned and sorted by allocatedCapacity in ascending order

                filter = ?start=0&count=5&sort=allocatedCapacity:asc&filter="provisionType='Thin'"

        :param filter: string with optional parameters to apply filtering and sorting operation
        """
        url = make_url(uri['storage-volumes'], filter=filter)

        body = get_members(self._con.get(url))
        return body

    def add_storage_volume(self, name=None, capacity=0, sto_pool_uri=None, shareable=None, is_permanent=True,
                           provision_type=None, description='', snapshot_uri=None, snapshot_pool_uri=None,
                           sto_system_uri=None, sto_system_volume_name=None, template_uri=None, wwn=None,
                           blocking=True, verbose=False):
        """Creates a volume on the storage system.

        :param name: name for the storage volume resource
        :param capacity: capacity requested for the volume in GiB
        :param sto_pool_uri: URI of storage pool from which the volume to be created
        :param shareable: describes if the volume is shareable (public) or private
        :param is_permanent: indicates that the volume will persist when the profile using this volume is deleted
        :param provision_type: provisioning type of the volume - Thin or Full
        :param description: description for the storage volume resource
        :param snapshot_uri: URI of the snapshot from which the volume has to be created
        :param snapshot_pool_uri: URI of the snapshot storage pool to be used for this volume
        :param sto_system_uri: URI of the storage system in which the volume to be created
        :param sto_system_volume_name: name of the volume on storage system to be added
        :param template_uri: URI of the storage volume template from which the volume will be created
        :param wwn: WWN of volume to be added

        :param blocking:
        :param verbose:
        """
        request = make_storage_volume_v3(name, capacity, sto_pool_uri, shareable, is_permanent, provision_type,
                                         description, snapshot_uri, snapshot_pool_uri, sto_system_uri,
                                         sto_system_volume_name, template_uri, wwn)

        task, body = self._con.post(uri['storage-volumes'], request)
        if blocking is True:
            task = self._activity.wait4task(task, tout=600, verbose=verbose)
            if 'type' in task and task['type'].startswith('Task'):
                entity = self._activity.get_task_associated_resource(task)
                volume = self._con.get(entity['resourceUri'])
                return volume
        return task

    def get_attachable_volumes(self, filter=''):
        """Gets the volumes that are connected on the specified networks based on the storage system port's expected
        network connectivity.

        A volume is attachable if it satisfies either of the following conditions:

        - The volume is shareable
        - The volume not shareable and not attached

        Examples:
            1 - Get all the attachable volumes managed by the appliance which are accessible over
            /rest/fc-networks/123-45-67 and /rest/fc-networks/111-222-333 networks.

                filter = ?query='availableNetworks IN [/rest/fc-networks/123-45-67,/rest/fc-networks/111-222-333]'

        :param filter: string with optional parameters to apply filtering and sorting operation
        """
        url = make_url(uri['attachable-volumes'], filter=filter)

        body = get_members(self._con.get(url))
        return body

    def get_volumes_repair(self, alert_fix_type='ExtraManagedStorageVolumePaths', filter=''):
        """Gets the list of extra managed storage volume paths.

        Examples:
            1 - Get the list of extra managed storage volume paths for the specified
            resourceUri='/rest/storage-volumes/AA-99-YY'

                filter = ?filter="resourceUri='/rest/storage-volumes/AA-99-YY'"

        :param filter: string with optional parameters to apply filtering and sorting operation
        :param alert_fix_type: type of alert fix of extra presentations from a storage volume
        """
        if filter:
            filter += '&alertFixType=' + alert_fix_type
        else:
            filter += '?alertFixType=' + alert_fix_type

        url = make_url(uri['volumes-repair'], filter=filter)

        body = get_members(self._con.get(url))
        return body

    def remove_volumes_repair_from_server(self, volume_uri, alert_fix_type='ExtraManagedStorageVolumePaths',
                                          blocking=True, verbose=False):
        """Removes extra presentations from a specified volume on the storage system.

        :param volume_uri: URI of specific server profile that will be removed extra presentations
        :param alert_fix_type: type of alert fix of extra presentations from a storage volume

        :param blocking:
        :param verbose:
        """
        request = {'type': alert_fix_type, 'resourceUri': volume_uri}

        task, body = self._con.post(uri['volumes-repair'], request)
        if blocking is True:
            task = self._activity.wait4task(task, tout=600, verbose=verbose)
            return body
        return task

    def get_storage_volume_by_id(self, volume_id):
        """Gets a volume by id.

        :param volume_id: ID of specific storage volume
        """
        url = make_url(uri['storage-volumes'], volume_id)

        body = self._con.get(url)
        return body

    def update_storage_volume(self, volume, force=False, blocking=True, verbose=False):
        """Updates properties of a volume.

        :param volume: the storage volume that will be updating
        :param force: if set to true the operation completes despite any problems with network connectivity or errors on
        the resource itself. The default is false.

        :param blocking:
        :param verbose:
        """
        url = make_url(volume['uri'], force=force)

        task, body = self._con.put(url, volume)
        if blocking is True:
            task = self._activity.wait4task(task, tout=600, verbose=verbose)
            return body
        return task

    def remove_storage_volume(self, volume_id, export_only=False, force=False, blocking=True, verbose=False):
        """Deletes a managed volume only from OneView or OneView and storage system.

        :param volume_id: ID of specific storage volume that will be removed
        :param export_only: indices if a volume will be removed only from OneView or OneView and storage system.
        :param force: if set to true the operation completes despite any problems with network connectivity or errors on
        the resource itself. The default is false.

        :param blocking:
        :param verbose:
        """
        ori_headers = self._con._headers
        url = make_url(uri['storage-volumes'], volume_id, force=force)
        if export_only:
            self._con._headers.update({'exportOnly': 'true'})

        task, body = self._con.delete(url)
        self._con._headers = ori_headers
        if blocking is True:
            task = self._activity.wait4task(task, tout=600, verbose=verbose)
            return body
        return task

    def add_snapshot_for_volume(self, volume_id, name='{volumeName}_{timestamp}', description='',
                                blocking=True, verbose=False):
        """Creates a snapshot for the volume specified

        :param volume_id: ID of specific storage volume
        :param name: name for the snapshot to be created
        :param description: description for the snapshot resource

        :param blocking:
        :param verbose:
        """
        url = make_url(uri['storage-volumes'], volume_id, 'snapshots')
        request = {'type': "Snapshot", 'name': name, 'description': description}

        task, body = self._con.post(url, request)
        if blocking is True:
            task = self._activity.wait4task(task, tout=600, verbose=verbose)
            return body
        return task

    def get_snapshot_of_volume(self, volume_id, snapshot_id):
        """Gets a snapshot of a volume

        :param volume_id: ID of specific storage volume
        :param snapshot_id: ID of specific snapshot that will be returned from a list of snapshots of specific volume
        """
        url = make_url(uri['storage-volumes'], volume_id, 'snapshots', snapshot_id)

        body = self._con.get(url)
        return body

    def remove_snapshot_from_volume(self, volume_id, snapshot_id, force=False, blocking=True, verbose=False):
        """Deletes a snapshot from OneView and storage system.

        :param volume_id: ID of specific storage volume
        :param snapshot_id: ID of specific snapshot
        :param force: if set to true the operation completes despite any problems with network connectivity or errors on
        the resource itself. The default is false.

        :param blocking:
        :param verbose:
        """
        url = make_url(uri['storage-volumes'], volume_id, 'snapshots', snapshot_id, force=force)

        task, body = self._con.delete(url)
        if blocking is True:
            task = self._activity.wait4task(task, tout=600, verbose=verbose)
            return body
        return task

    def get_snapshots_from_volume(self, volume_id, filter=''):
        """Gets all snapshots of a volume.

        Examples:
            1 - Get all snapshots in a storage volume (default)

                filter = ?start=0&count=-1

        :param volume_id: ID of specific storage volume
        :param filter: string with optional parameters to apply filtering and sorting operation
        """
        url = make_url(uri['storage-volumes'], volume_id, 'snapshots', filter=filter)

        body = get_members(self._con.get(url))
        return body

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
