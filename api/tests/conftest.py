"""
Common set of functionality for picoAPI testing.
Fixtures defined within this file are available to all
other testing modules.
"""

import pytest
import api.common
from pymongo import MongoClient

mongo_addr = "127.0.0.1"
mongo_port = 27017
mongo_db_name = "pico_test"

def setup_db():
    """ Creates a mongodb instance and shuts it down after testing has concluded. """

    client = MongoClient(mongo_addr, mongo_port)[mongo_db_name]

    if len(client.collection_names()) != 0:
        client.connection.drop_database(mongo_db_name)

    #Set debug client for mongo
    if api.common.external_client is None:
        api.common.external_client = client

    return client

def teardown_db():
    """ Drops the db and shuts down the mongodb instance. """
    client = MongoClient(mongo_addr, mongo_port)[mongo_db_name]
    client.connection.drop_database(mongo_db_name)
    client.connection.disconnect()
