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
    TAB_BOT = {'data': 'data', 'log': 'log', 'root': 'root'}
    USER_PERMISS = {}
    DB_CONT = {'login': None, 'name': None, 'passw': None, 'gender': None, 'phone': None, 'email': None}
    NAME_FIELD = {}
    NAME_FIELD['id'] = 'ID'
    NAME_FIELD['login'] = 'Логин'
    NAME_FIELD['passw'] = 'Пароль'
    NAME_FIELD['reg_date'] = 'Дата регистрации'
    NAME_FIELD['ch_date'] = 'Дата изменения'
    NAME_FIELD['name'] = 'Ф.И.О.'
    NAME_FIELD['gender'] = 'Пол'
    NAME_FIELD['phone'] = 'Номер телефона'
    NAME_FIELD['email'] = 'Эл.почта'
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
    CREATE_DBASE = 'Создать БД'
    DELETE_DBASE = 'Удалить БД'
    DATABASE_EXISTS = 'БД существует: '
    CREATE_DB_TAB = 'Создать таблицы'
    LIST_TABLES = 'Список таблиц'
#    DELETE_TABLES = 'Удалить таблицы'
    CREATE_SU_USER = 'Создать админа'
    CHENGE_PASSW_SU = 'Изменить пароль админа'
#===== Message ================
    SELECT_MENU = 'Выберите пункт меню: '
    NEW_USER = 'Login нового пользователя:'
    LOGIN = 'Login:'
    LOGIN_ERR = 'Ошибка, Login не существует! Введите Login:'
    EMAIL = 'Введите номер телефона:'
    PASSW = 'Введите пароль:'
    SUPERUSER = 'Создать админа'
    PASSW_OK = 'Поздравляю, вы ввели верный Login и Passwd'
    LOGIN_SUPERUSER = 'Введите Login админа'
    PASSW_SUPERUSER = 'Введите пароль админа'
    SU_CREATE = 'Админ создан'
    SU_CHENGE = 'Пароль админа изменен'
    DB_NO_CREATE = 'БД не создана'
    DB_OK = 'БД успешно создана'
    DB_DEL_OK = 'БД успешно удалена'
    DB_NO_DELETE = 'БД не удалена'
    DELET_DB = 'Для удаления БД введите: Удалить БД'
    TAB_OK = 'Таблицы созданы'
    FULL_SET = 'Поздравляю, вы выполнили основные настройки приложения.'
    PASSW_ERR = 'Ошибка, Passwd не верный. Введите Passwd:'
    NO_ACCESS = 'У вас нет прав: '
    UPDATE = 'Обновления и дополнительная информация: https://t.me/flaskbott'
    QUESTIONS = 'Вопросы и предложения:\n • @jwvsolmf\n • jwvsol@yandex.com'
# ======================================================================

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
    CHENGE_SU = '10'

