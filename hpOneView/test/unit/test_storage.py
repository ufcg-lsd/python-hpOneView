import mock
import uuid
import unittest

from hpOneView import storage
from hpOneView import connection

HOST = '1.2.3.4'


class StoragePoolsTestCase(unittest.TestCase):

    def setUp(self):
        super(StoragePoolsTestCase, self).setUp()
        self._con = connection(HOST)
        self._sto = storage(self._con)

    @mock.patch.object(connection, 'get')
    def test_get_storage_systems(self, mock_get):
        url = '/rest/storage-systems'

        self._sto.get_storage_systems()
        mock_get.assert_called_once_with(url)

        mock_get.reset_mock()
        url = '/rest/storage-systems?start=0&count=-1'

        self._sto.get_storage_systems(filter='?start=0&count=-1')
        mock_get.assert_called_once_with(url)

    @mock.patch.object(connection, 'post')
    def test_add_storage_system(self, mock_post):
        url = '/rest/storage-systems'

        mock_post.return_value = (None, None)
        request = {'ip_hostname': HOST, 'username': 'admin', 'password': 'pass'}

        # passing blocking as False because we just want to test the uri.
        self._sto.add_storage_system(host=HOST, user='admin', password='pass', blocking=False)
        mock_post.assert_called_once_with(url, request)

    @mock.patch.object(connection, 'get')
    def test_get_storage_systems_host_types(self, mock_get):
        url = '/rest/storage-systems/host-types'

        self._sto.get_storage_systems_host_types()
        mock_get.assert_called_once_with(url)

    @mock.patch.object(connection, 'get')
    def test_get_storage_pools_in_storage_system(self, mock_get):
        sto_system_id = uuid.uuid4().__str__()
        url = '/rest/storage-systems/{arrayId}/storage-pools'

        self._sto.get_storage_pools_in_storage_system(sto_system_id)
        mock_get.assert_called_once_with(url.format(arrayId=sto_system_id))

        mock_get.reset_mock()
        url = '/rest/storage-systems/{arrayId}/storage-pools?start=0&count=5'
        self._sto.get_storage_pools_in_storage_system(sto_system_id, filter='?start=0&count=5')
        mock_get.assert_called_once_with(url.format(arrayId=sto_system_id))

    @mock.patch.object(connection, 'get')
    def test_get_storage_system_by_id(self, mock_get):
        url = '/rest/storage-systems/{id}'
        sto_system_id = uuid.uuid4().__str__()

        self._sto.get_storage_system_by_id(sto_system_id)
        mock_get.assert_called_once_with(url.format(id=sto_system_id))

    @mock.patch.object(connection, 'put')
    def test_update_storage_system(self, mock_put):
        url = '/rest/storage-systems/{id}'
        sto_system_id = uuid.uuid4().__str__()

        mock_put.return_value = (None, None)
        sto_system = {'uri': url.format(id=sto_system_id)}

        # passing blocking as False because we just want to test the uri.
        self._sto.update_storage_system(sto_system, blocking=False)
        mock_put.assert_called_once_with(url.format(id=sto_system_id) + '?force=false', sto_system)

        mock_put.reset_mock()
        # passing blocking as False because we just want to test the uri.
        self._sto.update_storage_system(sto_system, force=True, blocking=False)
        mock_put.assert_called_once_with(url.format(id=sto_system_id) + '?force=true', sto_system)

    @mock.patch.object(connection, 'delete')
    def test_remove_storage_system(self, mock_delete):
        url = '/rest/storage-systems/{id}'
        sto_system_id = uuid.uuid4().__str__()

        mock_delete.return_value = (None, None)
        # passing blocking as False because we just want to test the uri.
        self._sto.remove_storage_system(sto_system_id, blocking=False)
        mock_delete.assert_called_once_with(url.format(id=sto_system_id) + '?force=false')

        mock_delete.reset_mock()
        # passing blocking as False because we just want to test the uri.
        self._sto.remove_storage_system(sto_system_id, force=True, blocking=False)
        mock_delete.assert_called_once_with(url.format(id=sto_system_id) + '?force=true')

    @mock.patch.object(connection, 'get')
    def test_get_storage_system_managed_ports(self, mock_get):
        url = '/rest/storage-systems/{id}/managedPorts'
        sto_system_id = uuid.uuid4().__str__()

        self._sto.get_storage_system_managed_ports(sto_system_id)
        mock_get.assert_called_once_with(url.format(id=sto_system_id))

        mock_get.reset_mock()
        url = '/rest/storage-systems/{id}/managedPorts?start=0&count=5&sort=portName:asc&filter=state=Normal'

        self._sto.get_storage_system_managed_ports(sto_system_id,
                                                   filter='?start=0&count=5&sort=portName:asc&filter=state=Normal')
        mock_get.assert_called_once_with(url.format(id=sto_system_id))

    @mock.patch.object(connection, 'get')
    def test_get_storage_system_managed_port_by_port_id(self, mock_get):
        url = '/rest/storage-systems/{id}/managedPorts/{portId}'
        port_id = uuid.uuid4().__str__()
        sto_system_id = uuid.uuid4().__str__()

        self._sto.get_storage_system_managed_port_by_port_id(sto_system_id, port_id)
        mock_get.assert_called_once_with(url.format(id=sto_system_id, portId=port_id))

    @mock.patch.object(connection, 'get')
    def test_get_storage_pools(self, mock_get):
        url = '/rest/storage-pools'

        self._sto.get_storage_pools()
        mock_get.assert_called_once_with(url)

        mock_get.reset_mock()
        url = '/rest/storage-pools?start=0&count=5&sort=freeCapacity:desc&filter=name=myName'

        self._sto.get_storage_pools(filter='?start=0&count=5&sort=freeCapacity:desc&filter=name=myName')
        mock_get.assert_called_once_with(url)

    @mock.patch.object(connection, 'post')
    def test_add_storage_pool(self, mock_post):
        url = '/rest/storage-pools'

        mock_post.return_value = (None, None)
        request = {'storageSystemUri': '/rest/storage-systems/111111', 'poolName': 'MyStoragePoll'}

        # passing blocking as False because we just want to test the uri.
        self._sto.add_storage_pool(name='MyStoragePoll', sto_system_uri='/rest/storage-systems/111111', blocking=False)
        mock_post.assert_called_once_with(url, request)

    @mock.patch.object(connection, 'get')
    def test_get_storage_pool_by_id(self, mock_get):
        url = '/rest/storage-pools/{id}'
        sto_pool_id = uuid.uuid4().__str__()

        self._sto.get_storage_pool_by_id(sto_pool_id)
        mock_get.assert_called_once_with(url.format(id=sto_pool_id))

    @mock.patch.object(connection, 'delete')
    def test_remove_storage_pool(self, mock_delete):
        url = '/rest/storage-pools/{id}'
        sto_pool_id = uuid.uuid4().__str__()

        mock_delete.return_value = (None, None)
        # passing blocking as False because we just want to test the uri.
        self._sto.remove_storage_pool(sto_pool_id=sto_pool_id, blocking=False)
        mock_delete.assert_called_once_with(url.format(id=sto_pool_id) + '?force=false')

        mock_delete.reset_mock()
        # passing blocking as False because we just want to test the uri.
        self._sto.remove_storage_pool(sto_pool_id=sto_pool_id, force=True, blocking=False)
        mock_delete.assert_called_once_with(url.format(id=sto_pool_id) + '?force=true')

    @mock.patch.object(connection, 'get')
    def test_get_attachments_volumes(self, mock_get):
        url = '/rest/storage-volume-attachments'

        self._sto.get_attachments_volumes()
        mock_get.assert_called_once_with(url)

        mock_get.reset_mock()
        url = '/rest/storage-volume-attachments?start=0&count=-1'

        self._sto.get_attachments_volumes(filter='?start=0&count=-1')
        mock_get.assert_called_once_with(url)

    @mock.patch.object(connection, 'get')
    def test_get_attachments_volumes_repair(self, mock_get):
        url = '/rest/storage-volume-attachments/repair'

        self._sto.get_attachments_volumes_repair()
        mock_get.assert_called_once_with(url + '?alertFixType=ExtraUnmanagedStorageVolumes')

    @mock.patch.object(connection, 'post')
    def test_remove_attachments_volumes_repair_from_server(self, mock_post):
        url = '/rest/storage-volume-attachments/repair'

        mock_post.return_value = (None, None)
        request = {'resourceUri': '/rest/server-profiles/123-45-67-89-124', 'type': 'ExtraUnmanagedStorageVolumes'}

        # passing blocking as False because we just want to test the uri.
        self._sto.remove_attachments_volumes_repair_from_server(server_uri='/rest/server-profiles/123-45-67-89-124',
                                                                blocking=False)
        mock_post.assert_called_once_with(url, request)

    @mock.patch.object(connection, 'get')
    def test_get_attachments_volumes_paths(self, mock_get):
        url = '/rest/storage-volume-attachments/{attachmentId}/paths'
        attachment_id = uuid.uuid4().__str__()

        self._sto.get_attachments_volumes_paths(attachment_id)
        mock_get.assert_called_once_with(url.format(attachmentId=attachment_id))

    @mock.patch.object(connection, 'get')
    def test_get_attachments_volumes_paths_by_id(self, mock_get):
        url = '/rest/storage-volume-attachments/{attachmentId}/paths/{id}'
        port_id = uuid.uuid4().__str__()
        attachment_id = uuid.uuid4().__str__()

        self._sto.get_attachments_volumes_paths_by_id(attachment_id, port_id)
        mock_get.assert_called_once_with(url.format(attachmentId=attachment_id, id=port_id))

    @mock.patch.object(connection, 'get')
    def test_get_attachments_volumes_by_id(self, mock_get):
        url = '/rest/storage-volume-attachments/{id}'
        attachment_id = uuid.uuid4().__str__()

        self._sto.get_attachments_volumes_by_id(attachment_id)
        mock_get.assert_called_once_with(url.format(id=attachment_id))

    @mock.patch.object(connection, 'get')
    def test_get_storage_volume_templates(self, mock_get):
        url = '/rest/storage-volume-templates'

        self._sto.get_storage_volume_templates()
        mock_get.assert_called_once_with(url)

        mock_get.reset_mock()
        url = '/rest/storage-volume-templates?start=0&count=-1'

        self._sto.get_storage_volume_templates(filter='?start=0&count=-1')
        mock_get.assert_called_once_with(url)

    @mock.patch.object(connection, 'post')
    def test_add_storage_volume_template(self, mock_post):
        url = '/rest/storage-volume-templates'

        mock_post.return_value = (None, None)
        request = {
            "name": "TemplateExample",
            "description": "Example Template",
            "provisioning": {
               "shareable": True,
               "provisionType": "Thin",
               "capacity": 21474836480,
               "storagePoolUri": "/rest/storage-pools/222222"
            },
            "storageSystemUri": "/rest/storage-systems/111111",
            "snapshotPoolUri": "/rest/storage-pools/222222",
            "type": "StorageVolumeTemplateV3"
        }

        # passing blocking as False because we just want to test the uri.
        self._sto.add_storage_volume_template(name='TemplateExample', capacity=20,
                                              sto_pool_uri='/rest/storage-pools/222222', shareable=True,
                                              provision_type='Thin', description='Example Template',
                                              sto_system_uri='/rest/storage-systems/111111',
                                              snapshot_pool_uri='/rest/storage-pools/222222', blocking=False)
        mock_post.assert_called_once_with(url, request)

    @mock.patch.object(connection, 'get')
    def test_get_connectable_storage_volume_templates(self, mock_get):
        url = '/rest/storage-volume-templates/connectable-volume-templates'

        self._sto.get_connectable_storage_volume_templates()
        mock_get.assert_called_once_with(url)

        mock_get.reset_mock()
        url = '/rest/storage-volume-templates/connectable-volume-templates?query=availableNetworks IN ' \
              '[/rest/fc-networks/123-45-67,/rest/fc-networks/111-222-333]'

        self._sto.get_connectable_storage_volume_templates(filter=
                                                           '?query=availableNetworks IN [/rest/fc-networks/123-45-67,' +
                                                           '/rest/fc-networks/111-222-333]')
        mock_get.assert_called_once_with(url)

    @mock.patch.object(connection, 'get')
    def test_get_storage_volume_template_by_id(self, mock_get):
        url = '/rest/storage-volume-templates/{id}'
        template_id = uuid.uuid4().__str__()

        self._sto.get_storage_volume_template_by_id(template_id)
        mock_get.assert_called_once_with(url.format(id=template_id))

    @mock.patch.object(connection, 'put')
    def test_update_storage_volume_template(self, mock_put):
        url = '/rest/storage-volume-templates/{id}'
        template_id = uuid.uuid4().__str__()

        mock_put.return_value = (None, None)
        template = {'uri': url.format(id=template_id)}

        # passing blocking as False because we just want to test the uri.
        self._sto.update_storage_volume_template(template, blocking=False)
        mock_put.assert_called_once_with(url.format(id=template_id) + '?force=false', template)

        mock_put.reset_mock()
        # passing blocking as False because we just want to test the uri.
        self._sto.update_storage_volume(template, force=True, blocking=False)
        mock_put.assert_called_once_with(url.format(id=template_id) + '?force=true', template)

    @mock.patch.object(connection, 'delete')
    def test_remove_storage_volume_template(self, mock_delete):
        url = '/rest/storage-volume-templates/{id}'
        template_id = uuid.uuid4().__str__()

        mock_delete.return_value = (None, None)
        # passing blocking as False because we just want to test the uri.
        self._sto.remove_storage_volume_template(template_id=template_id, blocking=False)
        mock_delete.assert_called_once_with(url.format(id=template_id) + '?force=false')

        mock_delete.reset_mock()
        # passing blocking as False because we just want to test the uri.
        self._sto.remove_storage_volume_template(template_id=template_id, force=True, blocking=False)
        mock_delete.assert_called_once_with(url.format(id=template_id) + '?force=true')

    @mock.patch.object(connection, 'get')
    def test_get_storage_volumes(self, mock_get):
        url = '/rest/storage-volumes'

        self._sto.get_storage_volumes()
        mock_get.assert_called_once_with(url)

        mock_get.reset_mock()
        url = '/rest/storage-volume-templates?start=0&count=5&sort=allocatedCapacity:asc&filter=provisionType=Thin'

        self._sto.get_storage_volume_templates(filter=
                                               '?start=0&count=5&sort=allocatedCapacity:asc&filter=provisionType=Thin')
        mock_get.assert_called_once_with(url)

    @mock.patch.object(connection, 'post')
    def test_add_storage_volume(self, mock_post):
        url = '/rest/storage-volumes'

        request = {
            "name": "TemplateExample",
            "description": "Example Template",
            "isPermanent": True,
            "provisioningParameters": {
               "shareable": True,
               "provisionType": "Thin",
               "requestedCapacity": 21474836480,
               "storagePoolUri": "/rest/storage-pools/222222"
            },
            "snapshotPoolUri": "/rest/storage-pools/222222",
            "storageSystemUri": "/rest/storage-systems/111111",
            "type": "AddStorageVolumeV3"
        }

        mock_post.return_value = (None, None)

        # passing blocking as False because we just want to test the uri.
        self._sto.add_storage_volume(name='TemplateExample', capacity=20, is_permanent=True,
                                     sto_pool_uri='/rest/storage-pools/222222', shareable=True,
                                     provision_type='Thin', description='Example Template',
                                     sto_system_uri='/rest/storage-systems/111111',
                                     snapshot_pool_uri='/rest/storage-pools/222222', blocking=False)
        mock_post.assert_called_once_with(url, request)

    @mock.patch.object(connection, 'get')
    def test_get_attachable_volumes(self, mock_get):
        url = '/rest/storage-volumes/attachable-volumes'

        self._sto.get_attachable_volumes()
        mock_get.assert_called_once_with(url)

        mock_get.reset_mock()
        url = '/rest/storage-volumes/attachable-volumes?query=availableNetworks IN ' \
              '[/rest/fc-networks/123-45-67,/rest/fc-networks/111-222-333]'

        self._sto.get_attachable_volumes(filter='?query=availableNetworks IN ' +
                                                '[/rest/fc-networks/123-45-67,/rest/fc-networks/111-222-333]')
        mock_get.assert_called_once_with(url)

    @mock.patch.object(connection, 'get')
    def test_get_volumes_repair(self, mock_get):
        url = '/rest/storage-volumes/repair'

        self._sto.get_volumes_repair()
        mock_get.assert_called_once_with(url + '?alertFixType=ExtraManagedStorageVolumePaths')

        mock_get.reset_mock()
        url = '/rest/storage-volumes/repair?filter=resourceUri=' \
              '/rest/storage-volumes/AA-99-YY&alertFixType=ExtraManagedStorageVolumePaths'

        self._sto.get_volumes_repair(filter='?filter=resourceUri=/rest/storage-volumes/AA-99-YY')
        mock_get.assert_called_once_with(url)

    @mock.patch.object(connection, 'post')
    def test_remove_volumes_repair_from_server(self, mock_post):
        url = '/rest/storage-volumes/repair'

        mock_post.return_value = (None, None)
        request = {'resourceUri': '/rest/storage-volumes/AA-99-YY', 'type': 'ExtraManagedStorageVolumePaths'}

        # passing blocking as False because we just want to test the uri.
        self._sto.remove_volumes_repair_from_server(volume_uri='/rest/storage-volumes/AA-99-YY',
                                                    blocking=False)
        mock_post.assert_called_once_with(url, request)

    @mock.patch.object(connection, 'get')
    def test_get_storage_volume_by_id(self, mock_get):
        url = '/rest/storage-volumes/{id}'
        volume_id = uuid.uuid4().__str__()

        self._sto.get_storage_volume_by_id(volume_id)
        mock_get.assert_called_once_with(url.format(id=volume_id))

    @mock.patch.object(connection, 'put')
    def test_update_storage_volume(self, mock_put):
        url = '/rest/storage-volumes/{id}'
        volume_id = uuid.uuid4().__str__()

        mock_put.return_value = (None, None)
        volume = {'uri': url.format(id=volume_id)}

        # passing blocking as False because we just want to test the uri.
        self._sto.update_storage_volume_template(volume, blocking=False)
        mock_put.assert_called_once_with(url.format(id=volume_id) + '?force=false', volume)

        mock_put.reset_mock()
        # passing blocking as False because we just want to test the uri.
        self._sto.update_storage_volume(volume, force=True, blocking=False)
        mock_put.assert_called_once_with(url.format(id=volume_id) + '?force=true', volume)

    @mock.patch.object(connection, 'delete')
    def test_remove_storage_volume(self, mock_delete):
        url = '/rest/storage-volumes/{id}'
        volume_id = uuid.uuid4().__str__()

        mock_delete.return_value = (None, None)
        # passing blocking as False because we just want to test the uri.
        self._sto.remove_storage_volume(volume_id=volume_id, blocking=False)
        mock_delete.assert_called_once_with(url.format(id=volume_id) + '?force=false')

        mock_delete.reset_mock()
        # passing blocking as False because we just want to test the uri.
        self._sto.remove_storage_volume(volume_id=volume_id, force=True, blocking=False)
        mock_delete.assert_called_once_with(url.format(id=volume_id) + '?force=true')

    @mock.patch.object(connection, 'post')
    def test_add_snapshot_for_volume(self, mock_post):
        url = '/rest/storage-volumes/{id}/snapshots'
        volume_id = uuid.uuid4().__str__()

        mock_post.return_value = (None, None)
        request = {'type': 'Snapshot', 'name': '{volumeName}_{timestamp}', 'description': 'Snapshot Example'}

        # passing blocking as False because we just want to test the uri.
        self._sto.add_snapshot_for_volume(volume_id=volume_id, description='Snapshot Example', blocking=False)
        mock_post.assert_called_once_with(url.format(id=volume_id), request)

    @mock.patch.object(connection, 'get')
    def test_get_snapshot_of_volume(self, mock_get):
        url = '/rest/storage-volumes/{id}/snapshots/{snapshotId}'
        volume_id = uuid.uuid4().__str__()
        snapshot_id = uuid.uuid4().__str__()

        self._sto.get_snapshot_of_volume(volume_id=volume_id, snapshot_id=snapshot_id)
        mock_get.assert_called_once_with(url.format(id=volume_id, snapshotId=snapshot_id))

    @mock.patch.object(connection, 'delete')
    def test_remove_snapshot_from_volume(self, mock_delete):
        url = '/rest/storage-volumes/{id}/snapshots/{snapshotId}'
        volume_id = uuid.uuid4().__str__()
        snapshot_id = uuid.uuid4().__str__()

        mock_delete.return_value = (None, None)
        # passing blocking as False because we just want to test the uri.
        self._sto.remove_snapshot_from_volume(volume_id=volume_id, snapshot_id=snapshot_id, blocking=False)
        mock_delete.assert_called_once_with(url.format(id=volume_id, snapshotId=snapshot_id) + '?force=false')

        mock_delete.reset_mock()
        mock_delete.return_value = (None, None)
        # passing blocking as False because we just want to test the uri.
        self._sto.remove_snapshot_from_volume(volume_id=volume_id, snapshot_id=snapshot_id,
                                              force=True, blocking=False)
        mock_delete.assert_called_once_with(url.format(id=volume_id, snapshotId=snapshot_id) + '?force=true')

    @mock.patch.object(connection, 'get')
    def test_get_snapshots_from_volume(self, mock_get):
        url = '/rest/storage-volumes/{volumeId}/snapshots'
        volume_id = uuid.uuid4().__str__()

        self._sto.get_snapshots_from_volume(volume_id=volume_id)
        mock_get.assert_called_once_with(url.format(volumeId=volume_id))

        mock_get.reset_mock()
        url = '/rest/storage-volumes/{volumeId}/snapshots?start=0&count=-1'

        self._sto.get_snapshots_from_volume(volume_id=volume_id, filter='?start=0&count=-1')
        mock_get.assert_called_once_with(url.format(volumeId=volume_id))









