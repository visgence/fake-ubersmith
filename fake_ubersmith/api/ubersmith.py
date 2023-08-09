"""Ubersmith Base"""
from flask import request

from fake_ubersmith.api.base import Base
from fake_ubersmith.api.utils.response import response


class UbersmithBase(Base):
    """Ubersmith Base"""
    def __init__(self, data_store):
        super().__init__(data_store)

        self.crash_mode = False

    def hook_to(self, entity):
        self.app = entity
        self.app.add_url_rule(
            '/api/2.0/',
            view_func=self._route_method,
            methods=["POST", "GET"]
        )

        self.register_endpoints(
            ubersmith_method='hidden.enable_crash_mode',
            function=self.enable_crash_mode
        )
        self.register_endpoints(
            ubersmith_method='hidden.disable_crash_mode',
            function=self.disable_crash_mode
        )

    def enable_crash_mode(self, form_data):
        """enable crash mode"""
        self.logger.info({f"Form data: {form_data}"})
        self.logger.info("Enabling crash-mode")
        self.crash_mode = True
        return response(data="Crash Mode Enabled")

    def disable_crash_mode(self, form_data):
        """disable crash mode"""
        self.logger.info({f"Form data: {form_data}"})
        self.logger.info("Disabling crash-mode")
        self.crash_mode = False
        return response(data="Crash Mode Disabled")

    def register_endpoints(self, ubersmith_method, function):
        """register endpoints"""
        self.methods[ubersmith_method] = function

    def _should_crash(self, method):
        return method not in [
            'hidden.enable_crash_mode',
            'hidden.disable_crash_mode'
        ] and self.crash_mode

    def _route_method(self):
        try:
            data = request.form.copy()
            method = data.pop("method")
        except Exception:
            data = request.form.copy()
            method = request.args.get("method")

        self.logger.info(
            f"Will call method '{method}' with params '{data}'"
        )

        if self._should_crash(method):
            self.logger.info("Will raise because crash-mode is enable")
            raise FakeUbersmithError(message="Crash mode was enabled")

        try:
            return self.methods[method](data)
        except Exception:
            self.logger.debug("Endpoint raised error", exc_info=True)
            raise


class FakeUbersmithError(Exception):
    """fake ubersmith error"""
    def __init__(self, code=None, message=None):
        self.code = code
        self.message = message
