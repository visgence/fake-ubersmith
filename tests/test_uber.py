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

import unittest
from unittest.mock import patch

from werkzeug.datastructures import ImmutableMultiDict

from fake_ubersmith.api.methods.uber import Uber
from fake_ubersmith.api.ubersmith import FakeUbersmithError


class TestUberModule(unittest.TestCase):

    def setUp(self):
        self.uber = Uber()

    @patch('fake_ubersmith.api.methods.uber.response')
    def test_service_plan_get_returns_if_service_plan_found(self, m_resp):
        self.uber.service_plans = [{"plan_id": 1}]

        m_resp.return_value = '{"data": {"plan_id": 1}, "error_code": null, ' \
                              '"error_message": "", "status": true}'

        self.assertEqual(
            self.uber.service_plan_get(form_data={"plan_id": 1}),
            '{"data": {"plan_id": 1}, "error_code": null, '
            '"error_message": "", "status": true}'
        )

        m_resp.assert_called_with(data={"plan_id": 1})

    @patch('fake_ubersmith.api.methods.uber.response')
    def test_service_plan_get_errs_if_service_plan_not_found(self, m_resp):
        self.uber.service_plans = [{"plan_id": 1}]

        m_resp.return_value = '{"data": None, "error_code": 3, ' \
                              '"error_message": "No Service Plan found", ' \
                              '"status": false}'

        self.assertEqual(
            self.uber.service_plan_get(form_data={"plan_id": 100}),
            '{"data": None, "error_code": 3, '
            '"error_message": "No Service Plan found", "status": false}'
        )

        m_resp.assert_called_with(error_code=3, message="No Service Plan found")

    @patch('fake_ubersmith.api.methods.uber.response')
    def test_service_plan_get_errs_with_service_plan_error(self, m_resp):
        self.service_plan_error = FakeUbersmithError(999, 'some error')

        m_resp.return_value = '{"data": None, "error_code": 999, ' \
                              '"error_message": "some error", ' \
                              '"status": false}'

        self.assertEqual(
            self.uber.service_plan_get(form_data={"plan_id": 100}),
            '{"data": None, "error_code": 999, '
            '"error_message": "some error", "status": false}'
        )

        m_resp.assert_called_with(error_code=3, message="No Service Plan found")

    @patch('fake_ubersmith.api.methods.uber.response')
    def test_service_plan_list_returns_all_plans(self, m_resp):

        self.uber.service_plans_list = {
            "1": {"code": "42"}, "2": {"code": "99"}
        }
        m_resp.return_value = '{"data": {"1": {"code": "42"}, ' \
                              '"2": {"code": "99"}}, ' \
                              '"error_code": null, "error_message": "", ' \
                              '"status": true' \
                              '}'

        self.assertEqual(
            self.uber.service_plan_list(form_data=ImmutableMultiDict([])),
            '{"data": {"1": {"code": "42"}, '
            '"2": {"code": "99"}}, '
            '"error_code": null, "error_message": "", "status": true}'
        )

        m_resp.assert_called_once_with(
            data={"1": {"code": "42"}, "2": {"code": "99"}}
        )

    @patch('fake_ubersmith.api.methods.uber.response')
    def test_service_plan_list_returns_plans_matching_code(self, m_resp):

        self.uber.service_plans_list = {
            "1": {"plan_id": "1", "code": "42"},
            "2": {"plan_id": "1", "code": "99"}
        }
        m_resp.return_value = '{"data": {"1": {"code": "42"}}, ' \
                              '"error_code": null, "error_message": "", ' \
                              '"status": true' \
                              '}'

        self.assertEqual(
            self.uber.service_plan_list(
                form_data=ImmutableMultiDict([('code', '42')])
            ),
            '{"data": {"1": {"code": "42"}}, '
            '"error_code": null, "error_message": "", "status": true}'
        )

        m_resp.assert_called_once_with(
            data={"1": {"plan_id": "1", "code": "42"}}
        )
