# -*- coding: utf-8 -*-
from rethinkdbcm import UseDatabase

class UseDB(object):
    def __init__(self, config: dict):
        self.config = config

# Проверка наличия записи в таблице
    def presence_id(self, use_db, name_t, id_mane, req):
        with UseDatabase(self.config, use_db) as db:
            try:
                return db.countid(name_t, id_mane, req)
            except:
                return False

# Создание БД
    def db_creat(self, use_db):
        with UseDatabase(self.config) as db:
            try:
                out = db.create_db(use_db)
#                print(out)
                return out
            except:
                return False

# Удаление БД
    def db_delete(self, use_db):
        with UseDatabase(self.config) as db:
            try:
                out = db.del_db(use_db)
#                print(out)
                return out
            except:
                return False

# Создание таблицы в БД
    def tab_creat(self, use_db, use_tab):
        with UseDatabase(self.config) as db:
            try:
                out = db.create_tab(use_db, use_tab)
#                print(out)
                return out
            except:
                return False

# Запрос всех таблиц в БД
    def tab_all(self, use_db):
        with UseDatabase(self.config) as db:
            try:
                out = db.all_table(use_db)
#                print(out)
                return out
            except:
                return False

# Удаление таблицы в БД
    def tab_delete(self, use_db, use_tab):
        with UseDatabase(self.config) as db:
            try:
                out = db.del_tab(use_db, use_tab)
#                print(out)
                return out
            except:
                return False
