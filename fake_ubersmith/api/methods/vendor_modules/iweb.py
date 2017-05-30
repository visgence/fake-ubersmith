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
from fake_ubersmith.api.base import Base
from fake_ubersmith.api.utils.response import response


class Iweb(Base):
    def __init__(self, data_store):
        super().__init__(data_store)

    def hook_to(self, entity):
        entity.register_endpoints(
            ubersmith_method='iweb.log_event',
            function=self.log_event
        )

    def log_event(self, form_data):
        self.data_store.event_log.append(form_data.to_dict())
        return response(data="1")
