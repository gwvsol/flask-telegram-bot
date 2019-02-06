from enum import Enum

class Config(object):
#===== Set Bot Telegram =======
    API_TOKEN = '742304158:AAFeunhPvTtDs7D4bJ8OG1XU3iJPVNyBbTY'
    WEBHOOK_HOST = 'srv00.hldns.ru'
    WEBHOOK_PORT = 8443                    # 443, 80, 88 or 8443 (port need to be 'open')
    WEBHOOK_LISTEN = '0.0.0.0'
    WEBHOOK_SSL_CERT = 'webhook_cert.pem'  # Path to the ssl certificate
    WEBHOOK_SSL_PRIV = 'webhook_pkey.pem'  # Path to the ssl private key
#===== Set Data Base ==========
    DB_CONFIG = { 'host': 'localhost', 'port': 28015, }
    DB_NAME = 'bot'
    DB_TAB = {'tab_1': 'chat_log', 'tab_2': 'app_log'}
    DB_CONT = {'id': None, 'login': None, 'name': None, 'passw': None, 'gender': None, 'phone': None, 'email': None}
#===== Message ================
    CREATE_USER = 'Создание нового пользователя'
    EDIT_PROFILE = 'Редактирование профиля'
    UPDATES = 'Обновления'
    FEEDBACK = 'Обратная связь'
    MAIN_MENU = 'Главное меню'
    SELECT_MENU = 'Выберите пункт меню:'
    NEW_USER = 'Login нового пользователя:'
    LOGIN = 'Login пользователя:'
    UPDATE = 'Обновления и дополнительная информация: https://t.me/flaskbott'
    QUESTIONS = 'Вопросы и предложения:\n • @jwvsolmf\n • jwvsol@yandex.com'

class Status(Enum):
    START = '0'  # Начало нового диалога
    LOGIN = '1'
    NAME = '2'
    PHONE = '3'
    EMAIL = '4'
    GENDER = '5'
    PASSW = '6'
