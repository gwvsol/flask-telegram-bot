# -*- coding: utf-8 -*-
from enum import Enum

class Config(object):
#===== Set Bot Telegram =======
    API_TOKEN = '742304158:AAFeunhPvTtDs7D4bJ8OG1XU3iJPVNyBbTY'
    WEBHOOK_HOST = 'srv00.hldns.ru'
    WEBHOOK_PORT = 8443                    # 443, 80, 88 or 8443 (port need to be 'open')
    WEBHOOK_LISTEN = '0.0.0.0'
    WEBHOOK_SSL_CERT = 'webhook_cert.pem'  # Path to the ssl certificate
    WEBHOOK_SSL_PRIV = 'webhook_pkey.pem'  # Path to the ssl private key
    ROOT_USER = {'login': 'root', 'passw': 'b4b8daf4b8ea9d39568719e1e320076f'}
#===== Set Data Base ==========
    DB_CONFIG = { 'host': 'localhost', 'port': 28015, }
    DB_NAME = {'db_bot': 'db_bot', 'db_api': 'data'}
    TAB_BOT = {'chat_log': 'chat_log', 'app_log': 'app_log', 'root': 'root'}
    TAB_API = {'data': 'data', 'log': 'log', 'root': 'root'}
    USER_PERMISS = {}
    DB_CONT = {'login': None, 'name': None, 'passw': None, 'gender': None, 'phone': None, 'email': None}
#========= Menu ===============
    USER_DATA = 'Данные пользователя'
    CREATE_USER = 'Создание'
    EDIT_PROFILE = 'Редактирование'
    PASSW_RECOV = 'Восстановление'
    SETTING = 'Настройка'
    BASK_SET = 'Возврат к настройкам'
    UPDATES = 'О приложении'
    FEEDBACK = 'Как связаться'
    MAIN_MENU = 'Главное меню'
    CREATE_DBASE = 'Создесть БД'
    CREATE_DB_TAB = 'Создать таблицы БД'
#===== Message ================
    SELECT_MENU = 'Выберите пункт меню: '
    NEW_USER = 'Login нового пользователя:'
    LOGIN = 'Login:'
    LOGIN_ERR = 'Ошибка, Login не существует! Введите Login:'
    EMAIL = 'Введите номер телефона:'
    PASSW = 'Введите пароль:'
    PASSW_OK = 'Поздравляю, вы ввели верный Login и Passwd'
    LOGIN_SUPERUSER = 'Введите Login суперпользователя'
    PASSW_SUPERUSER = 'Введите пароль суперпользователя'
    FULL_SET = 'Поздравляю, вы выполнили основные настройки приложения, теперь вы можете создать первого пользователя.'
    PASSW_ERR = 'Ошибка, Passwd не верный. Введите Passwd:'
    NO_ACCESS = 'У вас нет прав: '
    UPDATE = 'Обновления и дополнительная информация: https://t.me/flaskbott'
    QUESTIONS = 'Вопросы и предложения:\n • @jwvsolmf\n • jwvsol@yandex.com'

class Status(Enum):
    START = '0'  # Начало нового диалога
    LOGIN = '1'
    PASSW = '2'
    NAME = '3'
    PHONE = '4'
    EMAIL = '5'
    GENDER = '6'
    CHECKED = '7'
    SUPERUSER = '8'
    SUPER_PASS = '9'

