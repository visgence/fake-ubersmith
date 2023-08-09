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
from fake_ubersmith.api.ubersmith import FakeUbersmithError
from fake_ubersmith.api.utils.response import response


class Order(Base):
    """Order"""
    def __init__(self, data_store):
        super().__init__(data_store)

    def hook_to(self, entity):
        entity.register_endpoints(
            ubersmith_method='order.coupon_get',
            function=self.coupon_get
        )
        entity.register_endpoints(
            ubersmith_method='order.create',
            function=self.create_order
        )
        entity.register_endpoints(
            ubersmith_method='order.respond',
            function=self.order_respond
        )
        entity.register_endpoints(
            ubersmith_method='order.submit',
            function=self.submit_order
        )
        entity.register_endpoints(
            ubersmith_method='order.cancel',
            function=self.cancel_order
        )

    def coupon_get(self, form_data):
        """coupon get"""
        coupon = next(
            (
                cf for cf in self.data_store.coupons
                if cf["coupon"]["coupon_code"] == form_data["coupon_code"]
            ),
            None
        )
        if coupon is not None:
            self.logger.info(f"Retrieved coupon data: {coupon}")
            return response(data=coupon)
        else:
            self.logger.info("Getting coupon info failed")
            return response(
                error_code=1, message="could not get coupon info"
            )

    def create_order(self, form_data):
        """create order"""
        order = self.data_store.order.get(form_data['order_queue_id'])
        if isinstance(order, FakeUbersmithError):
            self.logger.info("Creating order failed")
            return response(
                error_code=order.code, message=order.message
            )
        self.logger.info(f"Creating order: {order}")
        return response(data=order)

    def order_respond(self, form_data):
        """order respond"""
        self.logger.info({f"Form data: {form_data}"})
        data = 8
        self.logger.info(f"order response: {data}")
        return response(data=data)

    def submit_order(self, form_data):
        """submit order"""
        order_submit = self.data_store.order_submit.get(form_data['order_id'])

        if isinstance(order_submit, FakeUbersmithError):
            self.logger.error("Order submitted failed.")
            return response(
                error_code=order_submit.code, message=order_submit.message
            )
        self.logger.info(f"Order submitted info: {order_submit}")
        return response(data=order_submit)

    def cancel_order(self, form_data):
        """cancel order"""
        order_cancel = self.data_store.order_cancel.get(form_data['order_id'])
        if isinstance(order_cancel, FakeUbersmithError):
            self.logger.error("Cancel order failed.")
            return response(
                error_code=order_cancel.code, message=order_cancel.message
            )
        self.logger.info(f"Cancelling order info: {order_cancel}")
        return response(data=order_cancel)
