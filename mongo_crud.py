# -*- coding: utf-8 -*-
"""
Mark Baligad
4-1 Milestone: Create and Read in Python
2025-03-31
"""

from pymongo import MongoClient
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId


class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, user, passwd, host, port, database, collection):
        # Initializing the MongoClient. This helps to
        # access the MongoDB databases and collections.
        # This is hard-wired to use the aac database, the
        # animals collection, and the aac user.
        # Definitions of the connection string variables are
        # unique to the individual Apporto environment.
        #
        # You must edit the connection variables below to reflect
        # your own instance of MongoDB!
        #
        # Connection Variables
        #
        USER = user #'aacuser'
        PASS = passwd #'SNHU1234'
        HOST = host #'nv-desktop-services.apporto.com'
        PORT = port #30047
        DB = database #'AAC'
        COL = collection #'animals'
        #
        # Initialize Connection
        #
        uri = f"mongodb://{USER}:{PASS}@{HOST}:{PORT}/{DB}?authSource=admin"
        self.client = MongoClient(uri)
        print(f"Connecting with URI: {uri}")
        
        self.database = self.client['%s' % (DB)]
        print(f"Set database: {DB}")
        
        self.collection = self.database['%s' % (COL)]
        print(f"Set collection: {COL}")

    def create(self, data):
        """
        Insert a document into the animals collection
        :param data: Dictionary of key/value pairs
        :return: True if successful, False otherwise
        """
        if data:
            try:
                self.collection.insert_one(data)
                return True
            except PyMongoError as e:
                print(f"Insert failed: {e}")
                return False
        else:
            print("Create failed: data parameter is empty")
            return False

    def read(self, query=None):
        """
        Finds documents in the animals collection
        :param query: Dictionary of key/value pairs for filter
        :return: List of matching documents, or empty list if none
        """
        if query is None:
            query = {}

        try:
            return list(self.collection.find(query))
        except PyMongoError as e:
            print(f"Read failed: {e}")
            return []

    def update(self, query, new_data):
        """
        Update a document in the animals collection based on the given query
        :param query: Dictionary of key/value pairs for filter (find the document)
        :param new_data: Dictionary of key/value pairs for new data (update fields)
        :return: The number of objects modified in the collection
        """
        if query and new_data:
            try:
                # To update one document, use update_one
                # To update multiple documents, use update_many
                result = self.collection.update_many(query, {'$set': new_data})

                # Check if any document was matched and modified
                if result.matched_count > 0:
                    print(f"Updated {result.modified_count} document(s).")
                    return result.matched_count
                else:
                    print("No documents matched the query.")
                    return 0
            except PyMongoError as e:
                print(f"Update failed: {e}")
                return 0
        else:
            print("Update failed: query or new_data is empty")
            return 0

    def delete(self, query):
        """
        Delete a document in the animals collection based on the given query
        :param query: Dictionary of key/value pairs for filter (find the document to delete)
        :return: The number of objects removed from the collection
        """
        if query:
            try:
                # Perform delete. This will delete only one document that matches the query.
                # To delete one document, use delete_one
                # To delete multiple documents, use delete_many
                result = self.collection.delete_many(query)

                # Check if any document was deleted
                if result.deleted_count > 0:
                    print(f"Deleted {result.deleted_count} document(s).")
                    return result.deleted_count
                else:
                    print("No documents matched the query.")
                    return 0
            except PyMongoError as e:
                print(f"Delete failed: {e}")
                return 0
        else:
            print("Delete failed: query is empty")
            return 0