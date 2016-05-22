import pymongo
import settings


class MongoConn:
    def __init__(self):
        self.conn = pymongo.MongoClient(
            settings.MONGODB_SERVER,
            settings.MONGODB_PORT,
            connect=False
        )
        self.db = self.conn[settings.MONGODB_DB]
        self.torrents_coll = self.db[settings.MONGODB_TORRENTS_COLLECTION]

