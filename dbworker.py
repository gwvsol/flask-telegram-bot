# -*- coding: utf-8 -*-
from rethinkdbcm import UseDatabase
from config import Config

USER1 = Config.USER_PERMISS
#USER1['187911336'] = '1'

class UseDB(object):
    def __init__(self, config: dict):
        self.config = config


# Проверка наличия записи в таблице
    def presence_id(self, use_db, name_t, id_mane, req):
        with UseDatabase(self.config) as db:
            try:
                print(use_db, name_t, id_mane, req)
                out = db.countid(use_db, name_t, id_mane, req)
                print(out)
                return out
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
                


# Новая запись в таблицу в БД 
# (при подключении к БД необходимо указать к какой БД подключаемся)
    def new_record(self, use_db, use_tab, json):
        with UseDatabase(self.config) as db:
            try:
                out = db.insert(use_db, use_tab, json)
#                print(out)
                return out
            except:
                return False


# Получение всех записей из таблицы БД 
# (при подключении к БД необходимо указать к какой БД подключаемся)
    def getall(self, use_db, use_tab):
        with UseDatabase(self.config) as db:
            try:
                out = db.gettasks(use_db, use_tab)
#                print(out)
                return out
            except:
                return False


# Получение записи о пользователе ROOT в БД
    def getrootuser(self, use_db, use_tab, req):
        with UseDatabase(self.config) as db:
            try:
                return db.getroot(use_db, use_tab)[req]
            except:
                return False


# Получение записей из таблицы БД по ID
    def getonetask(self, use_db, use_tab, id_name):
        with UseDatabase(self.config) as db:
            try:
                out = db.gettask(use_db, use_tab, id_name)
#                print(out)
                return out
            except:
                return False


# Обновление записей в таблице БД по ID 
    def updateonetask(self, use_db, use_tab, id_name, json):
        with UseDatabase(self.config) as db:
            try:
                out = db.updetask(use_db, use_tab, id_name, json)
#                print(out)
                return out
            except:
                return False


# Удаление записи в таблице БД по определнному ID
    def deleteonetask(self, use_db, use_tab, id_name):
        with UseDatabase(self.config) as db:
            try:
                out = db.delltask(use_db, use_tab, id_name)
#                print(out)
                return out
            except:
                return False


########################################################################
# Получение записей из таблицы БД по ID или если БД не доступна, 
# подменить временно на локальную переменную, необходимо при настройке 
# приложения, когда БД еще не настроена (нет БД с которой будет работать
# приложение и нет таблиц в БД)
    def getuserid(self, use_db, use_tab, id_name):
        with UseDatabase(self.config) as db:
#            print('newidrecord')
            try:
                d = db.gettask(use_db, use_tab, id_name)
                out = d if d else USER1
#                print(out)
                return out
            except:
                return False
########################################################################
