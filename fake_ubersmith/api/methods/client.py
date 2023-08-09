"""client endpoints"""
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

import pickle
import time

from fake_ubersmith.api.base import Base
from fake_ubersmith.api.ubersmith import FakeUbersmithError
from fake_ubersmith.api.utils.response import response
from fake_ubersmith.api.utils.utils import a_random_id


class Client(Base):
    """Client base"""
    def __init__(self, data_store):
        super().__init__(data_store)

        self.credit_card_response = 1
        self.credit_card_delete_response = True

    def hook_to(self, entity):
        entity.register_endpoints(
            ubersmith_method='client.cc_add',
            function=self.client_cc_add
        )
        entity.register_endpoints(
            ubersmith_method='client.cc_update',
            function=self.client_cc_update
        )
        entity.register_endpoints(
            ubersmith_method='client.cc_info',
            function=self.client_cc_info
        )
        entity.register_endpoints(
            ubersmith_method='client.cc_delete',
            function=self.client_cc_delete
        )
        entity.register_endpoints(
            ubersmith_method='client.get',
            function=self.client_get
        )
        entity.register_endpoints(
            ubersmith_method='client.get_all',
            function=self.client_get_all
        )
        entity.register_endpoints(
            ubersmith_method='client.add',
            function=self.client_add
        )
        entity.register_endpoints(
            ubersmith_method='client.update',
            function=self.client_update
        )
        entity.register_endpoints(
            ubersmith_method='client.contact_add',
            function=self.contact_add
        )
        entity.register_endpoints(
            ubersmith_method='client.contact_get',
            function=self.contact_get
        )
        entity.register_endpoints(
            ubersmith_method='client.contact_list',
            function=self.contact_list
        )
        entity.register_endpoints(
            ubersmith_method='client.contact_update',
            function=self.contact_update
        )
        entity.register_endpoints(
            ubersmith_method='client.contact_permission_list',
            function=self.contact_permission_list
        )
        entity.register_endpoints(
            ubersmith_method='client.contact_permission_set',
            function=self.contact_permission_set
        )

        entity.register_endpoints(
            ubersmith_method='client.metadata_single',
            function=self.client_metadata_single
        )

        entity.register_endpoints(
            ubersmith_method='client.metadata_get',
            function=self.client_metadata_single
        )
        entity.register_endpoints(
            ubersmith_method='uber.attachment_get',
            function=self.get_attachments
        )
        entity.register_endpoints(
            ubersmith_method='uber.attachment_list',
            function=self.get_attachments
        )
        entity.register_endpoints(
            ubersmith_method='client.invoice_count',
            function=self.get_invoice_count
        )
        entity.register_endpoints(
            ubersmith_method='client.service_count_status',
            function=self.get_attachments
        )

    def get_attachments(self, form_data):
        """get attachments"""
        self.logger.info({f"Form data: {form_data}"})
        return response(data=[])

    def get_invoice_count(self, form_data):
        """get invoice count"""
        self.logger.info({f"Form data: {form_data}"})
        return response(data=1)

    def client_add(self, form_data):
        """client add"""
        client_id = str(a_random_id())

        client_data = form_data.copy()
        client_data["clientid"] = client_id
        client_data["contact_id"] = str(0)
        client_data["email"] = client_data.get("email").replace(" ", "")

        if client_data.get("uber_login"):
            client_data["login"] = client_data.get("uber_login").replace(" ", "")
            del client_data["uber_login"]
        else:
            client_data["login"] = client_data["login"].replace(" ", "")
        if client_data.get("full_name"):
            real_name=client_data.get("full_name")
        else:
            real_name="Real Name"

        self.logger.info(f"Adding client data: {client_data}")

        self.data_store.clients.append(client_data)
        pickle.dump( self.data_store.clients, open( "fixtures/client.p", "wb" ) )
        self.contact_add(
            dict(
                client_id=client_id,
                description="Primary Contact",
                login="so_much_invalid_username",
                password="so_much_invalid_password",
                real_name=real_name,
                rwhois_contact=0,
                created=int(time.time()),
                active=1,
                phone='1234567890',
                email="contact1@example.com"
            )
        )

        return response(data=client_id)

    def client_update(self, form_data):
        """client update"""
        client_id = form_data.get("client_id")

        client = next(iter(filter(lambda e: e["clientid"] == client_id, self.data_store.clients)))
        self.logger.info(f"Updating client {client['clientid']} with {form_data}")

        self._update_if_present(client, "first", form_data, "first")
        self._update_if_present(client, "last", form_data, "last")
        self._update_if_present(client, "email", form_data, "email")
        self._update_if_present(client, "login", form_data, "uber_login")

        client_metadata = {k: v for k, v in form_data.items() if k.startswith('meta_')}
        if len(client_metadata) >= 1:
            self._update_client_metadata(client_id, client_metadata)

        return response(data=True)

    def client_get(self, form_data):
        """client get"""
        client_id = form_data.get("client_id") or form_data.get("user_login")
        client = self._client_get(client_id)
        if client is not None:
            client.pop("contact_id")
            if "uber_pass" in client:
                client.pop("uber_pass")
            if form_data.get("acls") == "1":
                client["acls"] = []

            self.logger.info(f"client data being returned {client}")
            return response(data=client)
        else:
            self.logger.info(f"Can't find client ID - {client_id}")
            return response(
                error_code=1,
                message=f"Client ID '{client_id}' not found."
            )

    def _client_get(self, client_id):
        """_client get"""
        client = next((
            _format_client_get(client.copy()) for client in self.data_store.clients if client["clientid"] == client_id
        ), None)

        return client

    def client_get_all(self, form_data):
        """client get all"""
        self.logger.info({f"Form data: {form_data}"})

        return response(data=self.data_store.clients)

    def contact_add(self, form_data):
        """contact add"""
        contact_id = str(a_random_id())

        contact_data = form_data.copy()
        contact_data["contact_id"] = contact_id
        contact_data["rwhois_contact"] = 0
        contact_data["login"] = "contact" + str(a_random_id())
        contact_data["active"] = 1
        self.data_store.contacts.append(contact_data)
        pickle.dump( self.data_store.contacts, open( "fixtures/contact.p", "wb" ) )

        self.logger.info(f"Contact info added: {contact_data}")

        return response(data=contact_id)

    def contact_get(self, form_data):
        """contact get"""
        if "user_login" in form_data:
            self.logger.info("Looking up contact info by user_login")
            return self._get_contact_response(
                "login", 'user_login', form_data['user_login']
            )
        elif "contact_id" in form_data:
            self.logger.info("Looking up contact info by contact_id")
            return self._get_contact_response(
                "contact_id", 'contact_id', form_data['contact_id']
            )

        self.logger.error("No valid user_login or contact_id specified")
        return response(error_code=1, message="No contact ID specified")

    def contact_list(self, form_data):
        """contact list"""
        if "client_id" in form_data:
            self.logger.info("Retrieving contact list by client_id")
            return self._get_all_contacts_response(
                "client_id", 'client_id', form_data['client_id']
            )

        self.logger.error("No valid client_id specified")
        return response(error_code=1, message="No valid client ID specified")

    def contact_update(self, form_data):
        """contact update"""
        contact_id = form_data.get("contact_id")

        contact = self._get_contact_from_id(contact_id)
        self.logger.info(f"Updating contact {contact['contact_id']} with {form_data}")

        self._update_if_present(contact, "real_name", form_data, "real_name")
        self._update_if_present(contact, "description", form_data, "description")
        self._update_if_present(contact, "phone", form_data, "phone")
        self._update_if_present(contact, "email", form_data, "email")
        self._update_if_present(contact, "login", form_data, "login")
        self._update_if_present(contact, "password", form_data, "password")
        self._update_if_present(contact, "rwhois_contact", form_data, "rwhois_contact")
        self._update_if_present(contact, "created", form_data, "created")
        self._update_if_present(contact, "active", form_data, "active")

        return response(data=True)

    def contact_permission_list(self, form_data):
        """contact permission list"""
        contact_id = form_data.get("contact_id")
        resource_name = form_data.get("resource_name")
        contact = self._get_contact_from_id(contact_id)

        self.logger.info(f"Gathering permission list for contact_id : {contact_id}")

        return response(data=contact.get(resource_name, default_permissions))

    def contact_permission_set(self, form_data):
        """contact permission set"""
        contact_id = form_data.get("contact_id")
        resource_name = form_data.get("resource_name")
        action = form_data.get("action")
        type = form_data.get("type")

        effective = dict(read=0, create=0, update=0, delete=0)

        contact = self._get_contact_from_id(contact_id)

        if not contact.get(resource_name):
            contact[resource_name] = {
                "123": {
                    "resource_id": "123",
                    "name": resource_name,
                    "parent_id": "",
                    "lft": "",
                    "rgt": "",
                    "active": "1",
                    "label": "Manage Contacts",
                    "actions": ["2", "1", "3", "4"],
                    "action": [],
                    "effective": effective
                }
            }
        else:
            effective.update(contact[resource_name]['123'].get('effective'))

        contact[resource_name]['123']['effective'][action] = 1 if type == "allow" else False

        return response(data='')

    def client_cc_add(self, form_data):
        """client cc add"""
        self.logger.info({f"Form data: {form_data}"})
        if isinstance(self.credit_card_response, FakeUbersmithError):
            return response(
                error_code=self.credit_card_response.code,
                message=self.credit_card_response.message
            )
        return response(data=self.credit_card_response)

    def client_cc_update(self, form_data):
        """client cc update"""
        self.logger.info({f"Form data: {form_data}"})
        if isinstance(self.credit_card_response, FakeUbersmithError):
            return response(
                error_code=self.credit_card_response.code,
                message=self.credit_card_response.message
            )
        return response(data=True)

    def client_cc_info(self, form_data):
        """client cc info"""
        # returns no error if providing parameters, only an empty list
        if "billing_info_id" in form_data:
            return response(
                data={
                    cc["billing_info_id"]: cc
                    for cc in self.data_store.credit_cards
                    if cc["billing_info_id"] == form_data["billing_info_id"]
                }
            )
        elif "client_id" in form_data:
            return response(
                data={
                    cc["billing_info_id"]: cc
                    for cc in self.data_store.credit_cards
                    if cc["clientid"] == form_data["client_id"]
                }
            )
        else:
            return response(
                error_code=1,
                message="request failed: client_id parameter not supplied"
            )

    def client_cc_delete(self, form_data):
        """client cc delete"""
        self.logger.info({f"Form data: {form_data}"})
        if isinstance(self.credit_card_delete_response, FakeUbersmithError):
            return response(
                error_code=self.credit_card_delete_response.code,
                message=self.credit_card_delete_response.message
            )
        return response(data=True)

    def client_metadata_single(self, form_data):
        """client metadata single"""
        client_id = form_data.get("client_id")
        metadata_name = form_data.get("variable")

        self.logger.info(f"Gathering metadata {metadata_name} for client: {client_id}")

        client_metadata = self.data_store.metadatas.get(client_id)
        if client_metadata is None:
            return response(data=[])

        metadata = client_metadata.get(metadata_name)
        if metadata is None:
            return response(data=[])

        return response(data=metadata)

    def _get_contact_from_id(self, contact_id):
        """_get contact from id"""
        return next(iter(filter(lambda e: e["contact_id"] == contact_id, self.data_store.contacts)))

    def _get_all_contacts_response(self, lookup_key, matcher_key, matcher_value):
        """_get all contact response"""
        contacts = {
            contact['contact_id']: contact
            for contact in self.data_store.contacts
            if contact[lookup_key] == matcher_value
        }

        return response(data=contacts) if contacts else response(
            error_code=1, message=f"Invalid {matcher_key} specified."
        )

    def _get_contact_response(self, lookup_key, matcher_key, matcher_value):
        """_get contact response"""
        contact = next((contact for contact in self.data_store.contacts if contact[lookup_key] == matcher_value), None)
        if contact:
            client = self._client_get(contact["client_id"])

            self.logger.info(f"Getting contact info: {contact} for client {client}")

            return response(data=_format_contact_get(contact, client))
        else:
            return response(
                error_code=1, message=f"Invalid {matcher_key} specified."
            )

    def _update_if_present(self, target, target_key, source, source_key):
        try:
            value = source[source_key]
        except KeyError:
            return

        self.logger.debug(f"Setting {target_key} to {value}")
        target[target_key] = value

    def _update_client_metadata(self, client_id, client_metadata):
        if client_id not in self.data_store.metadatas:
            self.data_store.metadatas[client_id] = {}

        [self._update_if_present(self.data_store.metadatas[client_id], metadata_name.replace('meta_', ''),
                                 client_metadata, metadata_name) for
         metadata_name in client_metadata.keys()]


def _format_contact_get(contact, client):
    output = contact.copy()
    if "@" in output.get("email", ""):
        email_fields = output["email"].split("@")
    else:
        email_fields = "", ""

    output["email_name"], output["email_domain"] = email_fields

    output["password"] = "{ssha1}whatver it's hashed"
    output["password_timeout"] = "0"
    output["password_changed"] = "1549657344"

    output["first"] = output.get("real_name", "")
    output["last"] = ""

    if client is not None:
        output["listed_company"] = client["listed_company"]

    return output


def _format_client_get(client):
    client["listed_company"] = client.get("company", "") \
                or f"{client.get('last', '')}, {client.get('first', '')}"
    return client


default_permissions = {
    "123": {
        "resource_id": "123",
        "name": "some permission name",
        "parent_id": "456",
        "lft": "1035",
        "rgt": "1036",
        "active": "1",
        "label": "some permission label",
        "actions": [
            "2",
            "1",
            "3",
            "4"
        ],
        "effective": {
            "read": 0,
            "create": 0,
            "update": 0,
            "delete": 0
        }
    }
}
