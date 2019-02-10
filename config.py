# -*- coding: utf-8 -*-
from enum import Enum

class Config(object):
# ====== debug mode ============
    DEBUG_MODE = True
# ===== Set Bot Telegram =======
    API_TOKEN = '742304158:AAFeunhPvTtDs7D4bJ8OG1XU3iJPVNyBbTY'
    WEBHOOK_HOST = 'srv00.hldns.ru'
    WEBHOOK_PORT = 8443                    # 443, 80, 88 or 8443 (port need to be 'open')
    WEBHOOK_LISTEN = '0.0.0.0'
    WEBHOOK_SSL_CERT = 'webhook_cert.pem'  # Path to the ssl certificate
    WEBHOOK_SSL_PRIV = 'webhook_pkey.pem'  # Path to the ssl private key
    ROOT_USER = {'login': 'root', 'passw': 'b4b8daf4b8ea9d39568719e1e320076f'}
# ===== Set Data Base ==========
    DB_CONFIG = { 'host': 'localhost', 'port': 28015, }
    DB_NAME = {'db_bot': 'db_bot', 'db_api': 'data'}
    TAB_BOT = {'data': 'data', 'log': 'log', 'root': 'root'}
# =============================
    USER_PERMISS = {}
# =============================
    ID = 'id'
    PAS = 'passw'
    LOGI = 'login'
    CHT = 'ch_date'
    UNAME = 'name'
    GEND = 'gender'
    PHONE = 'phone'
    EMAIL = 'email'
    DATA_REG = 'reg_date'
# ==============================
    NAME_FIELD = {}
    NAME_FIELD['id'] = 'ID'
    NAME_FIELD['login'] = 'Логин'
    NAME_FIELD['passw'] = 'Пароль'
    NAME_FIELD['reg_date'] = 'Дата регистрации'
    NAME_FIELD['ch_date'] = 'Дата изменения'
    NAME_FIELD['name'] = 'Ф.И.О'
    NAME_FIELD['gender'] = 'Пол'
    NAME_FIELD['phone'] = 'Номер телефона'
    NAME_FIELD['email'] = 'Эл.почта'
# ========= Menu ===============
    USER_DATA = 'Данные пользователя'
    CREATE_USER = 'Создание'
    EDIT_PROFILE = 'Редактирование'
    PASSW_RECOV = 'Восстановление'
    SETTING = 'Настройка'
    UPDATES = 'О приложении'
    FEEDBACK = 'Как связаться'
    MAIN_MENU = 'Главное меню'
    CREATE_DBASE = 'Создать БД'
    DELETE_DBASE = 'Удалить БД'
    CREATE_DB_TAB = 'Создать таблицы'
    LIST_TABLES = 'Список таблиц'
    CREATE_SU_USER = 'Создать админа'
    CHENGE_PASSW_SU = 'Изменить пароль админа'
    NAME_EDIT = 'Ф.И.О'
    PASSW_EDIT = 'Пароль'
    PHONE_EDIT = 'Телефон'
    EMAIL_EDIT = 'Адрес эл.почты'
    GENDER_EDIT = 'Половая принадлежность'
    DELETE_PROF = 'Удалить'
    # ===== Message ================
    SELECT_MENU = 'Выберите пункт меню: '
    NEW_USER = 'Login нового пользователя:'
    NEW_PASSW = 'Passwd нового пользователя:'
    NEW_CREATE = 'Поздравляю, новый пользователь создан'
    LOGIN_EXISTS = 'Извините, Login существует\nВведите новый Login:'
    LOGIN = 'Login:'
    LOGIN_ERR = 'Ошибка!\nLogin не существует\nВведите Login:'
    LOGIN_NO_VALID = 'Ошибка!\nLogin короткий,\nили содержит не допустимые символы'
    UGENDER = 'Укажите ваш пол'
    PASSW = 'Введите пароль:'
    PASSW_NEW = 'Введите новый пароль'
    PASSW_EDT = 'Пароль админа изменен'
    PASSW_OK = 'Поздравляю, вы ввели верный Login и Passwd'
    PASSW_ERR = 'Ошибка, Passwd не верный. Введите Passwd:'
    PASSW_USER_EDIT = 'Пароль изменен'
    PASSW_EXPLAN = """Пароль считается надежным, если:
• длина 8 или больше символов
• включает 1 или более цифру
• имеет 1 или более специальный символ
• имеет 1 или более символ в верхнем регистре
• имеет 1 или более символ в нижнем регистре"""
    PASSW_SIMPLE = 'Пароль простой\nВведите более сложный пароль'
    UPHONE = 'Введите номер телефона: \nНапример: \n79046755643\nили\n73832847222'
    PHONE_EDT = 'Номер телефона изменен'
    PHONE_ERR = 'Извините, вы ввели номер телефона в неверном формате'
    PHONE_NO_USER = 'Извините, указанный вами\nномер телефона не соответствует\nимеющемуся в БД'
    UEMAIL = 'Введите адрес эл. почты: \nНапример: \n mail@mail.ru'
    EMAIL_EDT = 'Адрес электронной почты изменен'
    EMAIL_ERR = 'Извините, вы ввели адрес эл. почты в неверном формате'
    EMAIL_NO_USER = 'Извините, указаный вами\nадрес эл. почты не соответствует\nимеющемуся в БД'
    UNAME_EDIT = 'Укажите пожалуйста, вашу Фамилию, Имя и Отчество\nОдной строкой, через пробел'
    UNAME_SAVE = 'Ваша Фамилия, Имя и Отчество\nсохранены в Базе данных'
    GENDER_SAVE = 'Данные о вашей половой принадлежности\nсохранены в Базе данных'
    LOGIN_SUPERUSER = 'Введите Login админа'
    PASSW_SUPERUSER = 'Введите пароль админа'
    DEL_CONFIRM = 'Вы действительно желаете\nудалить вашу учетную запись?\n• Да\n• Нет'
    DEL_COMPLITE = 'Удаление вашей\nучетной записи выполнено'
    NOT_DELETED = 'Отмена уделения'
    SUPERUSER = 'Создать админа'
    SU_CREATE = 'Админ создан'
    SU_CHENGE = 'Пароль админа изменен'
    DB_NO_CREATE = 'БД не создана'
    DB_OK = 'БД успешно создана'
    DB_DEL_OK = 'БД успешно удалена'
    DB_NO_DELETE = 'БД не удалена'
    DELET_DB = 'Для удаления БД введите: Удалить БД'
    TAB_OK = 'Таблицы созданы'
    FULL_SET = 'Поздравляю, вы выполнили основные настройки приложения.'
    NO_ACCESS = 'У вас нет прав: '
    UPDATE = 'Обновления и дополнительная информация: https://t.me/flaskbott'
    QUESTIONS = 'Вопросы и предложения:\n • @jwvsolmf\n • jwvsol@yandex.com'
    GUIDE_RECOVERY = 'Для восстановления пароля\nследуйте подсказкам гида'
# ======================================================================

class Status(Enum):
    START = '0'  # Начало нового диалога
    LOGIN_ROOT = '1'
    LOGIN_NEW = '11'
    LOGIN_USER = '100'
    LOGIN_RECOVER = '111'
    PASSW_ROOT = '2'
    PASSW_NEW = '22'
    PASSW_USER = '200'
    PASSW_EDIT = '220'
    PASSW_RECOVER = '222'
    EMAIL = '3'
    EMAIL_EDIT = '300'
    EMAIL_RECOVER = '30'
    PHONE = '4'
    PHONE_EDIT = '400'
    PHONE_RECOVER = '40'
    NAME = '5'
    GENDER = '6'
    CHECKED = '7'
    SUPERUSER = '8'
    SUPER_PASS = '9'
    CHENGE_SU = '10'
    EDIT = '50'
    DELETE = '500'

