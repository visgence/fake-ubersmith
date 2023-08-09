"""custom endpoints"""
from fake_ubersmith.api.base import Base


class UbersmithJoanBase(Base):
    """custom endpoints"""
    def __init__(self, data_store):
        super().__init__(data_store)

        self.crash_mode = False

    def hook_to(self, entity):
        self.app = entity
        self.app.add_url_rule(
            '/joan/clients/get_staff.php',
            view_func=self.get_staff_info,
            methods=["POST", "GET"]
        )
        self.app.add_url_rule(
            '/joan/clients/client_comments.php',
            view_func=self.get_comment_info,
            methods=["POST", "GET"]
        )

    def get_staff_info(self):
        """get staff info"""
        # staff_id = request.args.get("staff_id")

        try:
            return b'{"email": "staff1@example.com", "username": "staffuser1", "name": "Staff1"}'
        except Exception:
            self.logger.debug("Endpoint raised error", exc_info=True)
            raise

    def get_comment_info(self):
        """get comment info"""
        # client_id = request.args.get("client_id")

        try:
            return [{"comment_id": 123, "time": "1689180263", "user": "Staff1", \
"comment": "Comment 1", "edited": "1689180263", "editor": "Bob", \
"client_viewable": 1}]
        except Exception:
            self.logger.debug("Endpoint raised error", exc_info=True)
            raise

class FakeUbersmithError(Exception):
    """Fake Ubersmith"""
    def __init__(self, code=None, message=None):
        self.code = code
        self.message = message
