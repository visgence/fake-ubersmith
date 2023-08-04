# from flask import request

from fake_ubersmith.api.base import Base


class UbersmithJoanBase(Base):
    def __init__(self, data_store):
        super().__init__(data_store)

        self.crash_mode = False

    def hook_to(self, server):
        self.app = server
        self.app.add_url_rule(
            '/joan/clients/get_staff.php',
            view_func=self._staff_method,
            methods=["POST", "GET"]
        )
        self.app.add_url_rule(
            '/joan/clients/client_comments.php',
            view_func=self._comment_method,
            methods=["POST", "GET"]
        )
        
        self.register_endpoints(
            ubersmith_method='staff_id',
            function=self.get_staff_info
        )
        self.register_endpoints(
            ubersmith_method='client_id',
            function=self.get_comment_info
        )

    def register_endpoints(self, ubersmith_method, function):
        self.methods[ubersmith_method] = function

    def _staff_method(self):
        try:
            return self.methods['staff_id']()
        except Exception:
            self.logger.debug("Endpoint raised error", exc_info=True)
            raise

    def _comment_method(self):
        try:
            return self.methods['client_id']()
        except Exception:
            self.logger.debug("Endpoint raised error", exc_info=True)
            raise

    def get_staff_info(self):
        # staff_id = request.args.get("staff_id")

        try:
            import subprocess
            proc = subprocess.Popen("php /opt/fake_ubersmith/fake_ubersmith/joan/clients/get_staff.php", shell=True, stdout=subprocess.PIPE)
            response = proc.stdout.read()
            # self.logger.info('{}'.format(response), exc_info=True)
            return response
        except Exception:
            self.logger.debug("Endpoint raised error", exc_info=True)
            raise

    def get_comment_info(self):
        # client_id = request.args.get("client_id")

        try:
            import subprocess
            proc = subprocess.Popen("php /opt/fake_ubersmith/fake_ubersmith/joan/clients/client_comments.php", shell=True, stdout=subprocess.PIPE)
            response = proc.stdout.read()
            # self.logger.info('{}'.format(response), exc_info=True)
            return response
        except Exception:
            self.logger.debug("Endpoint raised error", exc_info=True)
            raise

class FakeUbersmithError(Exception):
    def __init__(self, code=None, message=None):
        self.code = code
        self.message = message
