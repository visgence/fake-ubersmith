"""load_fixtures"""
import pickle
import os
from fake_ubersmith.api.base import Base

class LoadFixtures(Base):
    """load fixture"""
    def __init__(self, data_store):
        super().__init__(data_store)

    def hook_to(self, entity):
        self.app = entity
        self.app.add_url_rule(
            '/api/2.0/load_fixtures',
            view_func=self.load_fixtures,
            methods=["POST", "GET"]
        )

    def load_fixtures(self):
        """load fixture"""
        files = []
        for file in os.listdir("/opt/fake_ubersmith/fixtures/"):
            if file.endswith(".p"):
                files.append(file)

        if len(files) > 0:
            print('flushing data')
            self.data_store.flush()
            client_ids = []

            for file in files:
                data = pickle.load( open( "/opt/fake_ubersmith/fixtures/" + file, "rb" ) )

                try:
                    if file.startswith("contact"):
                        print('importing contacts')
                        if isinstance(data, list):
                            for data_1 in data:
                                self.data_store.contacts.append(data_1)
                                # print(data_1)
                        else:
                            self.data_store.contacts.append(data)

                    if file.startswith("client"):
                        print('importing clients')
                        if isinstance(data, list):
                            for data_1 in data:
                                self.data_store.clients.append(data_1)
                                client_ids.append(data_1['clientid'])
                                # print(data_1)
                        else:
                            self.data_store.clients.append(data)

                except Exception:
                    print('Load Fixtures Failed')
                    return b'{"result": "failure"}'

            print('')
            print('*******************************************************************************************')
            print("To import clients into DMP, run the following commands in docker-inventory_app-1 container:")
            for client_id in client_ids:
                print(f"./manage.py ubersmith_migration --act client --client_id {client_id}")
            print('********************************************************************************************')
            print('')
            return b'{"result": "success"}'
