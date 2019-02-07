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

    def db_creat(self, use_db):
        with UseDatabase(self.config) as db:
            try:
                out = db.create_db(use_db)
                print(out)
                return out
            except:
                return False

    def db_delete(self, use_db):
        with UseDatabase(self.config) as db:
            try:
                out = db.del_db(use_db)
                print(out)
                return out
            except:
                return False

    def tab_creat(self, use_db, use_tab):
        with UseDatabase(self.config) as db:
            try:
                out = db.create_tab(use_db, use_tab)
                print(out)
                return out
            except:
                return False
                
    def tab_all(self, use_db):
        with UseDatabase(self.config) as db:
            try:
                out = db.all_table(use_db)
                print(out)
                return out
            except:
                return False
