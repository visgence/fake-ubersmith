import unittest
from unittest.mock import patch, Mock

from fake_ubersmith.api.administrative_local import AdministrativeLocal


class TestAdministrativeLocal(unittest.TestCase):
    def setUp(self):
        self.admin = AdministrativeLocal()

    def test_shutdown_works(self):
        patch_path = 'fake_ubersmith.api.administrative_local.request'
        environ_path = 'werkzeug.server.shutdown'

        with patch(patch_path, Mock(environ={environ_path: Mock()})) as m:
            self.admin.shutdown()
            self.assertTrue(m.environ.get('werkzeug.server.shutdown').called)

    def test_shutdown_raises(self):
        patch_path = 'fake_ubersmith.api.administrative_local.request'

        with patch(patch_path, Mock(environ={})):
            with self.assertRaises(RuntimeError):
                self.admin.shutdown()
