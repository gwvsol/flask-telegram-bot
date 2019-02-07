# -*- coding: utf-8 -*-
from rethinkdbcm import UseDatabase

class UseDB(object):
    def __init__(self, config: dict):
        self.config = config

    def presence_id(self, use_db, name_t, id_mane, req):
        with UseDatabase(self.config, use_db) as db:
            try:
                return db.countid(name_t, id_mane, req)
            except:
                return False
    
