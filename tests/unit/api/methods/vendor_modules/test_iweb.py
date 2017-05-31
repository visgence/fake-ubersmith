# Copyright 2017 Internap.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import json
import unittest

from flask import Flask

from fake_ubersmith.api.adapters.data_store import DataStore
from fake_ubersmith.api.methods.vendor_modules.iweb import IWeb
from fake_ubersmith.api.ubersmith import UbersmithBase


class TestIwebModule(unittest.TestCase):

    def setUp(self):
        self.data_store = DataStore()
        self.iweb = IWeb(self.data_store)

        self.app = Flask(__name__)
        self.base_iweb_api = UbersmithBase(self.data_store)

        self.iweb.hook_to(self.base_iweb_api)
        self.base_iweb_api.hook_to(self.app)

    def test_log_event_successfully(self):
        with self.app.test_client() as c:
            resp = c.post(
                'api/2.0/',
                data={
                    "method": "iweb.log_event",
                    "event_type": "Some event type",
                    "reference_type": "client",
                    "action": "Client Id 12345 performed a 'method'.",
                    "clientid": "clientid",
                    "user": "username",
                    "reference_id": "clientid"
                }
            )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            json.loads(resp.data.decode('utf-8')),
            {
                "data": "1",
                "error_code": None,
                "error_message": "",
                "status": True
            }
        )
        self.assertEqual(
            self.data_store.event_log[0],
            {
                "event_type": "Some event type",
                "reference_type": "client",
                "action": "Client Id 12345 performed a 'method'.",
                "clientid": "clientid",
                "user": "username",
                "reference_id": "clientid"
            }

        )
