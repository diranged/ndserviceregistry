import mock
import unittest

from mock import patch

from nd_service_registry import registration
from nd_service_registry import watcher


class DataNodeTests(unittest.TestCase):

    # A flag for filtering nose tests
    unit = True

    @patch.object(watcher.Watcher, 'add_callback')
    def test_data_node(self, mock_method):
        zk = mock.Mock()
        data = {'hello': 'world'}
        node = registration.DataNode(zk, '/service/path', data)
        self.assertEqual(node._data, data)
        self.assertFalse(node._ephemeral)
        mock_method.assert_called_once_with(node._update)

    @patch.object(watcher.Watcher, 'add_callback')
    def test_update(self, mock_method):
        zk = mock.Mock()
        initial_data = {'hello': 'world'}
        node = registration.DataNode(zk, '/service/path', initial_data)

        # Now, execute the _update() method with some new data and make
        # sure that the object updates itself properly.
        new_data = {'children': {},
                    'data': {"foo": "bar", "pid": "1234", "created": "test"},
                    'path': '/service/path',
                    'stat': None}
        node._update(new_data)
        self.assertEquals({"foo": "bar"}, node._data)
        self.assertTrue('pid' in node._encoded_data)
        self.assertTrue('created' in node._encoded_data)
        self.assertEquals(new_data['data'], node._decoded_data)


class EphemeralNodeTests(unittest.TestCase):

    # A flag for filtering nose tests
    unit = True

    @patch.object(watcher.Watcher, 'add_callback')
    def test_ephemeral_node(self, mock_method):
        zk = mock.Mock()
        data = {'hello': 'world'}
        node = registration.EphemeralNode(zk, '/service/path', data)
        self.assertEqual(node._data, data)
        self.assertTrue(node._ephemeral)
        mock_method.assert_called_once_with(node._update)
