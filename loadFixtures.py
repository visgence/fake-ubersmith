import pickle
import os

from fake_ubersmith.api.adapters.data_store import DataStore
data_store = DataStore()

files = []
for file in os.listdir("fixtures/"):
    if file.endswith(".p"):
         files.append(file)

if len(files) > 0:
     print('flushing data')
     data_store.flush()

for file in files:
        data = pickle.load( open( "fixtures/" + file, "rb" ) )

        if file.startswith("contact"):
            print('importing contacts')
            if type(data) is list:
                for d1 in data:
                    if type(d1) is dict:
                        for d2 in data:
                            data_store.contacts.append(d2)
                    else:
                         data_store.contacts.append(d1)
            else:
                 data_store.contacts.append(data)
                #  print(data)
        
        if file.startswith("client"):
            print('importing clients')
            if type(data) is list:
                for d1 in data:
                    data_store.clients.append(d1)
                    print(d1)
            else:
                 data_store.clients.append(data)
                #  print(data)
