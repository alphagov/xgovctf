"""
Common set of functionality for picoAPI testing.
Fixtures defined within this file are available to all
other testing modules.
"""

import pytest
from pymongo import MongoClient

mongo_addr = "127.0.0.1"
mongo_port = 27017
mongo_db_name = "pico_test"

@pytest.fixture(scope="session")
def db(request):
    """ Creates a mongodb instance and shuts it down after testing has concluded. """

    client = MongoClient(mongo_addr, mongo_port)[mongo_db_name]
    assert len(client.collection_names()) == 0, "Mongo db: {} is not empty.".format(mongo_db_name)

    def shutdown():
        """ Drops the db and shuts down the mongodb instance. """
        client.connection.drop_database(mongo_db_name)
        client.connection.disconnect()
        print("Disclientected from mongodb.")

    request.addfinalizer(shutdown)
    return client
