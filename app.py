# -*- coding: utf-8 -*-
from flask import Flask, request, abort
from dbworker import UseDB
from hashlib import md5
from datetime import datetime
from config import Config
from config import Status
import logging
import telebot
from telebot import types
import time
import re


logger = telebot.logger
telebot.logger.setLevel(logging.INFO)


app = Flask(__name__)
app.config.from_object(Config)
bot = telebot.TeleBot(app.config['API_TOKEN'])

#============ Bot ===============================
WEBHOOK_PORT = app.config['WEBHOOK_PORT']
WEBHOOK_LISTEN = app.config['WEBHOOK_LISTEN']
WEBHOOK_URL_BASE = 'https://{}:{}'.format(app.config['WEBHOOK_HOST'], app.config['WEBHOOK_PORT'])
WEBHOOK_URL_PATH = '/%s/'.format(app.config['API_TOKEN'])
WEBHOOK_SSL_CERT = app.config['WEBHOOK_SSL_CERT']
WEBHOOK_SSL_PRIV = app.config['WEBHOOK_SSL_PRIV']
#============ Data Base =========================
DB_CONF = app.config['DB_CONFIG']
DB_BOT = app.config['DB_NAME']['db_bot']
TAB_DATA = app.config['TAB_BOT']['data']
TAB_LOG = app.config['TAB_BOT']['log']
TAB_ROOT = app.config['TAB_BOT']['root']
ROOT_LOGIN = app.config['ROOT_USER']['login']
ROOT_PASSW = app.config['ROOT_USER']['passw']
USER = app.config['USER_PERMISS']
#USER[187911336] = '1'
DB = UseDB(DB_CONF)
ST = Status
NAME = app.config['NAME_FIELD']
ID, PAS, LOGI, CHT, GEND, PHONE, EMAIL, DATA_REG, UNAME = \
    app.config['ID'], app.config['PAS'], \
    app.config['LOGI'], app.config['CHT'], \
    app.config['GEND'], app.config['PHONE'], \
    app.config['EMAIL'], app.config['DATA_REG'], \
    app.config['UNAME']

# ============= Сохранение состояния пользователя бота =================
def save_state(id_bot=None, logn=None, pas=None, st=None, \
    gend=None, ph=None, em=None, name=None, res=False):
    s = DB.presence_id(DB_BOT, TAB_LOG, ID, str(id_bot))
    djson = {}  # Пустой временный словарь для данных в таблицу log
    djson[CHT] = datetime.now().strftime("%Y-%m-%d %X")
    djson[str(id_bot)] = st if id_bot else None  # Состояние в котором находится пользователь бота
    if logn or res:
        djson[LOGI] = logn if not res else 'xxxxxxxxx'
    if pas or res:
        djson[PAS] = pas if not res else 'xxxxxxxxx'
    if gend or res:
        djson[GEND] = gend if not res else 'xxxxxxxxx'
    if ph or res:
        djson[PHONE] = ph if not res else 'xxxxxxxxx'
    if em or res:
        djson[EMAIL] = em if not res else 'xxxxxxxxx'
    if name or res:
        djson[UNAME] = name if not res else 'xxxxxxxxx'
    if s == 1:  # Если таблица log в БД доступна обновляем БД
        DB.updateonetask(DB_BOT, TAB_LOG, str(id_bot), djson)
    elif s == 0: # Если таблица log есть но нет в ней записей, создаем их
        djson[ID] = str(id_bot)
        djson[DATA_REG] = datetime.now().strftime("%Y-%m-%d %X")
        db = DB.new_record(DB_BOT, TAB_LOG, djson)
        # Если таблица log в БД нет, пишем все во временную локальную переменную
        if 'the table does not exist' in str(db):
            USER.update(djson)
    print(djson)
    print(DB.getuserid(DB_BOT, TAB_LOG, str(id_bot)))


# ======================================================================
# =============== Проверка валидности адреса эл. почты =================
def isValidEmail(email):
    if len(email) > 7:
        if re.match(r'^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$', email) != None:
            return True
    return False
# =============== Проверка валидности номера телефона ==================
def isValidPhone(phone):
    if len(phone) > 7:
        if re.match(r'^((8|\+7|\+359)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', phone) != None:
            return True
    return False
# ======================================================================


# ======================================================================
# =========== Проверка пароля и его шифрование =========================
def setpasswd(login: str, passw: str) -> str:
    """Преобразование пароля и логина в хеш MD5"""
    return str(md5(str(passw+login).lower().encode('utf-8')).hexdigest())
    
def verify(id_bot, username=None, password=None):
    """Проверка пароля и логина"""
    if not password and username: # Только для проверки Login админа
        root_db = DB.getrootuser(DB_BOT, TAB_ROOT, LOGI)
        if root_db and DB.presence_id(DB_BOT, TAB_ROOT, ID, username) == 1:
            return DB.getonetask(DB_BOT, TAB_ROOT, username)[ID]
        elif not root_db and username and username == ROOT_LOGIN:
            return ROOT_LOGIN
        else:
            return None
    elif not username and password: # Только для проверки Passwd админа
        root_db = DB.getrootuser(DB_BOT, TAB_ROOT, LOGI)
        if root_db:
            logn = DB.getuserid(DB_BOT, TAB_LOG, id_bot)[LOGI]
            pas = setpasswd(logn, password)
        else:
            pas = setpasswd(ROOT_LOGIN, password)
        if root_db and DB.presence_id(DB_BOT, TAB_ROOT, PAS, pas) == 1:
            return DB.getonetask(DB_BOT, TAB_ROOT, logn)[PAS]
        elif not root_db and password and pas == ROOT_PASSW:
            return ROOT_PASSW
        else:
            return None
    else:
        return None
# ======================================================================

#===================== Bot Telegram ====================================
# Старт бота
@bot.message_handler(commands=['start'])
def handle_text(message):
    save_state(id_bot=str(message.chat.id), st=ST.START.value, res=True)
    user_markup = types.ReplyKeyboardMarkup(True, False)
    user_markup.row(app.config['USER_DATA'])
    user_markup.row(app.config['CREATE_USER'], app.config['PASSW_RECOV'])
    user_markup.row(app.config['UPDATES'], app.config['FEEDBACK'])
    bot.send_message(message.from_user.id, \
    app.config['SELECT_MENU'], reply_markup=user_markup)

# ================== Основное меню бота ================================
@bot.message_handler(func=lambda message: app.config['MAIN_MENU'] == \
    message.text, content_types=['text'])
def main_menu(message):
    save_state(id_bot=str(message.chat.id), st=ST.START.value, res=True)
    user_markup = types.ReplyKeyboardMarkup(True, False)
    user_markup.row(app.config['USER_DATA'])
    user_markup.row(app.config['CREATE_USER'], app.config['PASSW_RECOV'])
    user_markup.row(app.config['UPDATES'], app.config['FEEDBACK']) 
    bot.send_message(message.from_user.id, app.config['SELECT_MENU'], \
        reply_markup=user_markup) 
    
#================== О приложении, как связяться ========================
@bot.message_handler(func=lambda message: app.config['UPDATES'] == \
    message.text, content_types=['text'])
def handle_text(message):
    save_state(id_bot=str(message.chat.id), st=ST.START.value, res=True)
    user_markup = types.ReplyKeyboardMarkup(True, False)
    user_markup.row(app.config['MAIN_MENU'])
    bot.send_message(message.chat.id, \
    app.config['UPDATE'], reply_markup=user_markup)


@bot.message_handler(func=lambda message: app.config['FEEDBACK'] == \
    message.text, content_types=['text'])
def handle_text(message):
    save_state(id_bot=str(message.chat.id), st=ST.START.value, res=True)
    user_markup = types.ReplyKeyboardMarkup(True, False)
    user_markup.row(app.config['MAIN_MENU'])
    bot.send_message(message.chat.id, \
    app.config['QUESTIONS'], reply_markup=user_markup)
#=======================================================================

# ======================================================================
# =========== Запрос данных пользователя ===============================
# Запрос Login пользователя
@bot.message_handler(func=lambda message: app.config['USER_DATA'] \
    == message.text, content_types=['text'])
def user_data(message):
    save_state(id_bot=str(message.chat.id), st=ST.LOGIN_USER.value)
    user_markup = types.ReplyKeyboardMarkup(True, False)
    user_markup.row(app.config['MAIN_MENU'])
    user_markup.row(app.config['UPDATES'], app.config['FEEDBACK'])
    bot.send_message(message.from_user.id, \
        app.config['LOGIN'], reply_markup=user_markup)

# ============== Запрос Passwd пользователя ============================
@bot.message_handler(func=lambda message:
    DB.getuserid(DB_BOT, TAB_LOG, str(message.chat.id))[str(message.chat.id)] == \
    ST.LOGIN_USER.value)
def get_login(message):
    if DB.presence_id(DB_BOT, TAB_DATA, ID, str(message.text)):
        save_state(id_bot=str(message.chat.id), logn=message.text.lower(), \
        st=ST.PASSW_USER.value)
        user_markup = types.ReplyKeyboardMarkup(True, False)
        user_markup.row(app.config['MAIN_MENU'])
        user_markup.row(app.config['UPDATES'], app.config['FEEDBACK'])
        bot.send_message(message.from_user.id, \
            app.config['PASSW'], reply_markup=user_markup)
    else:
        bot.send_message(message.from_user.id, app.config['LOGIN_ERR'])
        return

# ================= Вывод данных пользователя ==========================
@bot.message_handler(func=lambda message:
    DB.getuserid(DB_BOT, TAB_LOG, str(message.chat.id))[str(message.chat.id)] == \
    ST.PASSW_USER.value)
def get_pass(message):
    logn = DB.getuserid(DB_BOT, TAB_LOG, str(message.chat.id))[LOGI]
    pas = setpasswd(logn, message.text)
    if DB.getuserid(DB_BOT, TAB_DATA, logn)[PAS] == pas:
        save_state(id_bot=str(message.chat.id), logn=message.text, pas=pas, \
        st=ST.EDIT.value)
        user_markup = types.ReplyKeyboardMarkup(True, False)
        user_markup.row(app.config['MAIN_MENU'], app.config['EDIT_PROFILE'])
        user_markup.row(app.config['UPDATES'], app.config['FEEDBACK'])
        for i in list(DB.getonetask(DB_BOT,TAB_DATA, logn).items()):
            if i[0] == 'passw':
                bot.send_message(message.from_user.id, \
                    '{}: {}'.format(NAME[i[0]], '**************'))
            else:
                bot.send_message(message.from_user.id, \
                    '{}: {}'.format(NAME[i[0]], i[1]))
        bot.send_message(message.from_user.id, \
            app.config['SELECT_MENU'], reply_markup=user_markup)
    else:
        bot.send_message(message.from_user.id, app.config['PASSW_ERR'])
        return


# ======================================================================
# ============= Редактирование пароля пользователя =====================
@bot.message_handler(func=lambda message:app.config['PASSW_EDIT'] == \
    message.text, content_types=['text'])
def edit_phone(message):
    save_state(id_bot=str(message.chat.id), st=ST.PASSW_EDIT.value)
    user_markup = types.ReplyKeyboardMarkup(True, False)
    user_markup.row(app.config['MAIN_MENU'], app.config['EDIT_PROFILE'])
    user_markup.row(app.config['UPDATES'], app.config['FEEDBACK'])
    bot.send_message(message.from_user.id, \
        app.config['PASSW'], reply_markup=user_markup)

@bot.message_handler(func=lambda message: 
    DB.getuserid(DB_BOT, TAB_LOG, str(message.chat.id))[str(message.chat.id)] == \
    ST.PASSW_EDIT.value)
def edit_phone(message):
    save_state(id_bot=str(message.chat.id), st=ST.EDIT.value)
    user_markup = types.ReplyKeyboardMarkup(True, False)
    user_markup.row(app.config['MAIN_MENU'], app.config['EDIT_PROFILE'])
    user_markup.row(app.config['UPDATES'], app.config['FEEDBACK'])
    bot.send_message(message.from_user.id, \
        app.config['PASSW'], reply_markup=user_markup)

# =========== Редактирование телефона пользователя =====================
@bot.message_handler(func=lambda message:app.config['PHONE_EDIT'] == \
    message.text, content_types=['text'])
def edit_pass(message):
    save_state(id_bot=str(message.chat.id), st=ST.EDIT.value)
    user_markup = types.ReplyKeyboardMarkup(True, False)
    user_markup.row(app.config['MAIN_MENU'], app.config['EDIT_PROFILE'])
    user_markup.row(app.config['UPDATES'], app.config['FEEDBACK'])
    bot.send_message(message.from_user.id, \
        app.config['UPHONE'], reply_markup=user_markup)

# ======= Редактирование адреса эл. почты пользователя =================
@bot.message_handler(func=lambda message:app.config['EMAIL_EDIT'] == \
    message.text, content_types=['text'])
def edit_email(message):
    save_state(id_bot=str(message.chat.id), st=ST.EDIT.value)
    user_markup = types.ReplyKeyboardMarkup(True, False)
    user_markup.row(app.config['MAIN_MENU'], app.config['EDIT_PROFILE'])
    user_markup.row(app.config['UPDATES'], app.config['FEEDBACK'])
    bot.send_message(message.from_user.id, \
        app.config['UEMAIL'], reply_markup=user_markup)

# =============== Редактирование пола пользователя =====================
@bot.message_handler(func=lambda message:app.config['GENDER_EDIT'] == \
    message.text, content_types=['text'])
def edit_gender(message):
    save_state(id_bot=str(message.chat.id), st=ST.EDIT.value)
    user_markup = types.ReplyKeyboardMarkup(True, False)
    user_markup.row(app.config['MAIN_MENU'], app.config['EDIT_PROFILE'])
    user_markup.row(app.config['UPDATES'], app.config['FEEDBACK'])
    bot.send_message(message.from_user.id, \
        app.config['UGENDER'], reply_markup=user_markup)

# =============== Удаление учетной записи пользователя =================
@bot.message_handler(func=lambda message:app.config['DELETE_PROF'] == \
    message.text, content_types=['text'])
def delete_prof(message):
    save_state(id_bot=str(message.chat.id), st=ST.START.value)
    user_markup = types.ReplyKeyboardMarkup(True, False)
    user_markup.row(app.config['MAIN_MENU'])
    user_markup.row(app.config['UPDATES'], app.config['FEEDBACK'])
    bot.send_message(message.from_user.id, \
        app.config['UDELETE'], reply_markup=user_markup)

# =============== Изменение данных пользователя ========================
# ======= Основное меню редактирования данных пользователя =============
@bot.message_handler(func=lambda message: 
    DB.getuserid(DB_BOT, TAB_LOG, str(message.chat.id))[str(message.chat.id)] == \
    ST.EDIT.value)
def edit_menu(message):
    user_markup = types.ReplyKeyboardMarkup(True, False)
    save_state(id_bot=str(message.chat.id), st=ST.EDIT.value)
    user_markup.row(app.config['MAIN_MENU'], app.config['PASSW_EDIT'])
    user_markup.row(app.config['PHONE_EDIT'], app.config['EMAIL_EDIT'])
    user_markup.row(app.config['DELETE_PROF'], app.config['GENDER_EDIT'])
    user_markup.row(app.config['UPDATES'], app.config['FEEDBACK'])
    bot.send_message(message.from_user.id, \
        app.config['SELECT_MENU'], reply_markup=user_markup)


# ======================================================================
# =============== Создание нового пользователя =========================
# ==================== Запрос нового логина ============================
@bot.message_handler(func=lambda message: app.config['CREATE_USER'] \
    == message.text, content_types=['text'])
def new_user(message):
    save_state(id_bot=message.chat.id, st=ST.LOGIN_NEW.value)
    user_markup = types.ReplyKeyboardMarkup(True, False)
    user_markup.row(app.config['MAIN_MENU'])
    user_markup.row(app.config['UPDATES'], app.config['FEEDBACK'])
    bot.send_message(message.from_user.id, \
        app.config['NEW_USER'], reply_markup=user_markup)

# ============ Сохранение логина и запрос нового пароля ================
@bot.message_handler(func=lambda message: 
        DB.getuserid(DB_BOT, TAB_LOG, str(message.chat.id))[str(message.chat.id)] == \
        ST.LOGIN_NEW.value)
def new_passw(message):
    print(DB.presence_id(DB_BOT, TAB_DATA, ID, str(message.text)))
    if not DB.presence_id(DB_BOT, TAB_DATA, ID, str(message.text.lower())):
        save_state(id_bot=message.chat.id, logn=message.text.lower(), \
        st=ST.PASSW_NEW.value)
        user_markup = types.ReplyKeyboardMarkup(True, False)
        user_markup.row(app.config['MAIN_MENU'])
        user_markup.row(app.config['UPDATES'], app.config['FEEDBACK'])
        bot.send_message(message.from_user.id, \
            app.config['NEW_PASSW'], reply_markup=user_markup)
    else:
        bot.send_message(message.chat.id, app.config['LOGIN_EXISTS'])
        return

# ============= Сохранение пароля и запрос адреса эл. почты ============
@bot.message_handler(func=lambda message: 
        DB.getuserid(DB_BOT, TAB_LOG, str(message.chat.id))[str(message.chat.id)] == \
        ST.PASSW_NEW.value)
def new_email(message):
    usr = DB.getuserid(DB_BOT, TAB_LOG, str(message.chat.id))
    pas = setpasswd(usr[LOGI], message.text)
    save_state(id_bot=message.chat.id, pas=pas, st=ST.EMAIL.value)
    user_markup = types.ReplyKeyboardMarkup(True, False)
    user_markup.row(app.config['MAIN_MENU'])
    user_markup.row(app.config['UPDATES'], app.config['FEEDBACK'])
    bot.send_message(message.from_user.id, \
        app.config['UEMAIL'], reply_markup=user_markup)

# =========== Сохранение адреса эл. почты и запрос номера телефона =====
@bot.message_handler(func=lambda message: 
        DB.getuserid(DB_BOT, TAB_LOG, str(message.chat.id))[str(message.chat.id)] == \
        ST.EMAIL.value)
def new_email(message):
    if isValidEmail(message.text):
        save_state(id_bot=message.chat.id, em=message.text, st=ST.PHONE.value)
        user_markup = types.ReplyKeyboardMarkup(True, False)
        user_markup.row(app.config['MAIN_MENU'])
        user_markup.row(app.config['UPDATES'], app.config['FEEDBACK'])
        bot.send_message(message.from_user.id, \
            app.config['UPHONE'], reply_markup=user_markup)
    else:
        bot.send_message(message.chat.id, app.config['ERR_EMAIL'])
        bot.send_message(message.chat.id, app.config['UEMAIL'])
        return

# ======= Сохранение номера телефона и создаем нового пользователя =====
@bot.message_handler(func=lambda message: 
        DB.getuserid(DB_BOT, TAB_LOG, str(message.chat.id))[str(message.chat.id)] == \
        ST.PHONE.value)
def NewUserCreate(message):
    if isValidPhone(message.text):
        save_state(id_bot=message.chat.id, ph=message.text, st=ST.PHONE.value)
        usr = DB.getuserid(DB_BOT, TAB_LOG, str(message.chat.id))
        new_usr = {}
        new_usr[ID] = usr[LOGI]
        new_usr[PAS] = usr[PAS]
        new_usr[LOGI] = usr[LOGI]
        new_usr[CHT] = datetime.now().strftime("%Y-%m-%d %X")
        new_usr[PHONE] = usr[PHONE]
        new_usr[EMAIL] = usr[EMAIL]
        new_usr[DATA_REG] = datetime.now().strftime("%Y-%m-%d %X")
        DB.new_record(DB_BOT, TAB_DATA, new_usr)
        user_markup = types.ReplyKeyboardMarkup(True, False)
        user_markup.row(app.config['MAIN_MENU'])
        user_markup.row(app.config['UPDATES'], app.config['FEEDBACK'])
        for i in list(DB.getonetask(DB_BOT,TAB_DATA, usr[LOGI]).items()):
            if i[0] == 'passw':
                bot.send_message(message.from_user.id, \
                    '{}: {}'.format(NAME[i[0]], '**************'))
            else:
                bot.send_message(message.from_user.id, \
                    '{}: {}'.format(NAME[i[0]], i[1]))
        bot.send_message(message.from_user.id, \
            app.config['NEW_CREATE'], reply_markup=user_markup)
    else:
        bot.send_message(message.chat.id, app.config['ERR_PHONE'])
        bot.send_message(message.chat.id, app.config['UPHONE'])
        return
# ======================================================================

# ======================================================================
# =========== Восстановление пароля пользователя =======================
@bot.message_handler(func=lambda message: app.config['PASSW_RECOV'] \
    == message.text, content_types=['text'])
def main_menu(message):
    user_markup = types.ReplyKeyboardMarkup(True, False)
    user_markup.row(app.config['MAIN_MENU'])
    user_markup.row(app.config['UPDATES'], app.config['FEEDBACK'])
    bot.send_message(message.from_user.id, \
        app.config['EMAIL'], reply_markup=user_markup)


# ======================================================================
# ================= Меню Настройка приложения ==========================
@bot.message_handler(commands=['setting'])
def main_menu(message):
    save_state(id_bot=message.chat.id, st=ST.LOGIN_ROOT.value, res=True)
    user_markup = types.ReplyKeyboardMarkup(True, False)
    user_markup.row(app.config['MAIN_MENU'])
    user_markup.row(app.config['UPDATES'], app.config['FEEDBACK'])
    bot.send_message(message.from_user.id, \
        app.config['LOGIN'], reply_markup=user_markup)


# ================ Запрос Login для аторизации =========================
@bot.message_handler(func=lambda message: \
    DB.getuserid(DB_BOT, TAB_LOG, str(message.chat.id))[str(message.chat.id)] == \
    ST.LOGIN_ROOT.value)
def user_entering_name(message):
    if verify(str(message.chat.id), username=message.text) == message.text:
        save_state(id_bot=message.chat.id, logn=message.text, st=ST.PASSW_ROOT.value)
        bot.send_message(message.chat.id, app.config['PASSW'])
    else:
        bot.send_message(message.chat.id, app.config['LOGIN_ERR'])
        return


# == Запрос Passwd для аторизации, Удаление БД и Создание таблиц в БД ==
@bot.message_handler(func=lambda message: \
    DB.getuserid(DB_BOT, TAB_LOG, str(message.chat.id))[str(message.chat.id)] == \
    ST.PASSW_ROOT.value)
def user_entering_passw(message):
    usr = DB.getuserid(DB_BOT, TAB_LOG, str(message.chat.id))
    if verify(str(message.chat.id), password=message.text) == \
        setpasswd(usr[LOGI].lower(), message.text):
        passw = setpasswd(usr[LOGI].lower(), message.text)
        save_state(id_bot=message.chat.id, pas=passw, st=ST.CHECKED.value)
        bot.send_message(message.chat.id, app.config['PASSW_OK'])
        user_markup = types.ReplyKeyboardMarkup(True, False)
        user_markup.row(app.config['MAIN_MENU'])
        # Если нет БД, выводим меню Создать БД
        if DB_BOT not in DB.db_creat(DB_BOT).keys():
            user_markup.row(app.config['CREATE_DBASE'])
            user_markup.row(app.config['UPDATES'], app.config['FEEDBACK'])
        # Если БД имеется, но нет таблиц выводим меню Создать таблицы и Удалить БД
        else: 
            m = 'not found' 
            if m in str(DB.tab_all(DB_BOT)):
                user_markup.row(app.config['CREATE_DB_TAB'], \
                    app.config['DELETE_DBASE'])
             # Если таблицы имеются, выводим меню Просмотр списка таблиц, 
             # Удалить таблицы и Удалить БД
            else:
                user_markup.row(app.config['LIST_TABLES'])
                if not DB.getrootuser(DB_BOT, TAB_ROOT, LOGI):
                    user_markup.row(app.config['DELETE_DBASE'], \
                        app.config['CREATE_SU_USER'])
                else:
                    user_markup.row(app.config['DELETE_DBASE'], \
                        app.config['CHENGE_PASSW_SU'])
            user_markup.row(app.config['UPDATES'], app.config['FEEDBACK'])
        bot.send_message(message.from_user.id, \
                app.config['SELECT_MENU'], reply_markup=user_markup)
    else:
        bot.send_message(message.chat.id, app.config['PASSW_ERR'])
        return


# ============= Создаем БД для приложения ==============================
@bot.message_handler(func=lambda message: app.config['CREATE_DBASE'] \
    == message.text, content_types=['text'])
def set_db(message):
    user_markup = types.ReplyKeyboardMarkup(True, False)
    user_markup.row(app.config['MAIN_MENU'])
    if DB.getuserid(DB_BOT, TAB_LOG, str(message.chat.id))[str(message.chat.id)] \
        == ST.CHECKED.value:
        save_state(id_bot=message.chat.id, st=ST.CHECKED.value)
        DB.db_creat(DB_BOT)
        if DB_BOT not in DB.db_creat(DB_BOT).keys():
            user_markup.row(app.config['CREATE_DBASE'])
            user_markup.row(app.config['UPDATES'], app.config['FEEDBACK'])
            bot.send_message(message.from_user.id, \
                app.config['DB_NO_CREATE'], reply_markup=user_markup)
        else:
            user_markup.row(app.config['CREATE_DB_TAB'])
            user_markup.row(app.config['UPDATES'], app.config['FEEDBACK'])
            bot.send_message(message.from_user.id, \
                app.config['DB_OK'], reply_markup=user_markup)
        bot.send_message(message.from_user.id, \
                app.config['SELECT_MENU'], reply_markup=user_markup)
    else:
        user_markup.row(app.config['UPDATES'], app.config['FEEDBACK'])
        bot.send_message(message.chat.id, app.config['NO_ACCESS'] + \
            app.config['CREATE_DBASE'])


# ==================== Удаление БД приложения ==========================
@bot.message_handler(func=lambda message: app.config['DELETE_DBASE'] \
    == message.text, content_types=['text'])
def set_db(message):
    save_state(id_bot=message.chat.id, st=ST.CHECKED.value)
    user_markup = types.ReplyKeyboardMarkup(True, False)
    user_markup.row(app.config['MAIN_MENU'])
    if DB.getuserid(DB_BOT, TAB_LOG, str(message.chat.id))[str(message.chat.id)] \
        == ST.CHECKED.value:
        if DB_BOT not in DB.db_delete(DB_BOT).keys():
            user_markup.row(app.config['CREATE_DBASE'])
            user_markup.row(app.config['UPDATES'], app.config['FEEDBACK'])
            bot.send_message(message.from_user.id, \
                app.config['DB_DEL_OK'], reply_markup=user_markup)
            bot.send_message(message.from_user.id, \
                app.config['SELECT_MENU'], reply_markup=user_markup)
        else:
            user_markup.row(app.config['DELETE_DBASE'])
            user_markup.row(app.config['UPDATES'], app.config['FEEDBACK'])
            bot.send_message(message.from_user.id, \
                app.config['DB_NO_DELETE'], reply_markup=user_markup)
            bot.send_message(message.from_user.id, \
                app.config['SELECT_MENU'], reply_markup=user_markup)
    else:
        user_markup = types.ReplyKeyboardMarkup(True, False)
        user_markup.row(app.config['MAIN_MENU'])
        user_markup.row(app.config['UPDATES'], app.config['FEEDBACK'])
        bot.send_message(message.chat.id, app.config['NO_ACCESS'] \
            + app.config['CREATE_DBASE'])


# ============= Создаем таблицы в БД для приложения ====================
@bot.message_handler(func=lambda message: app.config['CREATE_DB_TAB'] \
    == message.text, content_types=['text'])
def set_tab(message):
    if DB.getuserid(DB_BOT, TAB_LOG, str(message.chat.id))[str(message.chat.id)] \
        == ST.CHECKED.value:
        save_state(id_bot=message.chat.id, st=ST.CHECKED.value)
        user_markup = types.ReplyKeyboardMarkup(True, False)
        user_markup.row(app.config['MAIN_MENU'])
        name = list(app.config['TAB_BOT'].values())
        t = 0
        a = 0
        for n in range(len(name)):
            m = DB.tab_creat(DB_BOT, name[n])
            ok = 'tables_created'
            if ok in list(m.keys()):
                t += 1
                bot.send_message(message.chat.id, \
                    'Таблица {} {} создана'.format(t, name[n]))
            else:
                a += 1
                bot.send_message(message.chat.id, \
                    'Таблица {} {} уже существует'.format(a, name[n]))
        if a:
            user_markup.row(app.config['LIST_TABLES'])
            user_markup.row(app.config['UPDATES'], app.config['FEEDBACK'])
            bot.send_message(message.from_user.id, \
                app.config['SELECT_MENU'], reply_markup=user_markup)
        elif t:
            save_state(id_bot=message.chat.id, st=ST.SUPERUSER.value)
            user_markup.row(app.config['UPDATES'], app.config['FEEDBACK'])
            bot.send_message(message.from_user.id, app.config['TAB_OK'])
            bot.send_message(message.from_user.id, app.config['SUPERUSER'])
            bot.send_message(message.from_user.id, \
                app.config['LOGIN_SUPERUSER'], reply_markup=user_markup)
    else:
        user_markup.row(app.config['UPDATES'], app.config['FEEDBACK'])
        bot.send_message(message.chat.id, app.config['NO_ACCESS'] \
            + app.config['CREATE_DB_TAB'], reply_markup=user_markup)


# ====================== Перечень таблиц в БД ==========================
@bot.message_handler(func=lambda message: app.config['LIST_TABLES'] \
    == message.text, content_types=['text'])
def set_db(message):
    if DB.getuserid(DB_BOT, TAB_LOG, str(message.chat.id))[str(message.chat.id)] \
        == ST.CHECKED.value:
        for m in DB.tab_all(DB_BOT):
            bot.send_message(message.from_user.id, \
                'Таблица {} в БД {}'.format(m, DB_BOT))
        user_markup = types.ReplyKeyboardMarkup(True, False)
        user_markup.row(app.config['MAIN_MENU'])
        user_markup.row(app.config['UPDATES'], app.config['FEEDBACK'])
        bot.send_message(message.from_user.id, \
            app.config['SELECT_MENU'], reply_markup=user_markup)


# Удаление таблиц в БД
# Функция по удалению таблиц, без удаления БД конфликтует с системой аутентификации
# Требуется доработка
#@bot.message_handler(func=lambda message: app.config['DELETE_TABLES'] \
#    == message.text, content_types=['text'])
#def set_db(message):
#    if DB.getuserid(DB_BOT, TAB_LOG, str(message.chat.id))[str(message.chat.id)] \
#        == ST.CHECKED.value:
#        for m in DB.tab_all(DB_BOT):
#            DB.tab_delete(DB_BOT, m)
#            bot.send_message(message.from_user.id, \
#                'Таблица {} удалена из БД {}'.format(m, DB_BOT))
#        user_markup = types.ReplyKeyboardMarkup(True, False)
#        user_markup.row(app.config['MAIN_MENU'], app.config['CREATE_DB_TAB'])
#        user_markup.row(app.config['UPDATES'], app.config['FEEDBACK'])
#        bot.send_message(message.from_user.id, \
#            app.config['SELECT_MENU'], reply_markup=user_markup)


# =============== Cоздание суперпользователя ===========================
@bot.message_handler(func=lambda message: app.config['CREATE_SU_USER'] \
    == message.text, content_types=['text'])
def get_login_super(message):
    save_state(id_bot=message.chat.id, st=ST.SUPERUSER.value)
    user_markup = types.ReplyKeyboardMarkup(True, False)
    user_markup.row(app.config['MAIN_MENU'])
    user_markup.row(app.config['UPDATES'], app.config['FEEDBACK'])
    bot.send_message(message.from_user.id, app.config['SUPERUSER'])
    bot.send_message(message.from_user.id, \
        app.config['LOGIN_SUPERUSER'], reply_markup=user_markup)


# ============= Запрос Login для создания суперпользователя ============
@bot.message_handler(func=lambda message: \
    DB.getuserid(DB_BOT, TAB_LOG, str(message.chat.id))[str(message.chat.id)] == \
    ST.SUPERUSER.value)
def get_pass_super(message):
    save_state(id_bot=message.chat.id, logn=message.text, st=ST.SUPER_PASS.value)
    bot.send_message(message.from_user.id, app.config['PASSW_SUPERUSER'])


# ============= Запрос Passwd для создания суперпользователя ===========
@bot.message_handler(func=lambda message: \
    DB.getuserid(DB_BOT, TAB_LOG, str(message.chat.id))[str(message.chat.id)] == \
    ST.SUPER_PASS.value)
def set_superuser(message):
    usr = DB.getuserid(DB_BOT, TAB_LOG, str(message.chat.id))
    pas = setpasswd(usr[LOGI], message.text)
    save_state(id_bot=message.chat.id, pas=pas, st=ST.SUPER_PASS.value)
    usr = DB.getuserid(DB_BOT, TAB_LOG, str(message.chat.id))
    adm = {}
    adm['id'] = usr[LOGI].lower()
    adm['login'] = adm['id']
    adm['passw'] = usr[PAS]
    adm['reg_date'] = datetime.now().strftime("%Y-%m-%d %X")
    adm['ch_date'] = adm['reg_date']
    DB.new_record(DB_BOT, TAB_ROOT, adm)
    for i in list(DB.getonetask(DB_BOT, TAB_ROOT, adm['login']).items()):
        if i[0] == 'passw':
            bot.send_message(message.from_user.id, \
                '{}: {}'.format(NAME[i[0]], '**************'))
        else:
            bot.send_message(message.from_user.id, \
                '{}: {}'.format(NAME[i[0]], i[1]))
    user_markup = types.ReplyKeyboardMarkup(True, False)
    user_markup.row(app.config['MAIN_MENU'])
    user_markup.row(app.config['UPDATES'], app.config['FEEDBACK'])
    bot.send_message(message.from_user.id, app.config['SU_CREATE'])
    bot.send_message(message.chat.id, app.config['SELECT_MENU'], \
        reply_markup=user_markup)
        
        
# ================= Изменение пароля админа ============================
@bot.message_handler(func=lambda message: app.config['CHENGE_PASSW_SU'] \
    == message.text, content_types=['text'])
def get_new_pass_super(message):
    save_state(id_bot=message.chat.id, st=ST.CHENGE_SU.value)
    user_markup = types.ReplyKeyboardMarkup(True, False)
    user_markup.row(app.config['MAIN_MENU'])
    user_markup.row(app.config['UPDATES'], app.config['FEEDBACK'])
    bot.send_message(message.from_user.id, app.config['CHENGE_PASSW_SU'])
    bot.send_message(message.from_user.id, \
        app.config['PASSW_SUPERUSER'], reply_markup=user_markup)
        

# ================== Обновление пароля админа ==========================
@bot.message_handler(func=lambda message: \
    DB.getuserid(DB_BOT, TAB_LOG, str(message.chat.id))[str(message.chat.id)] == \
    ST.CHENGE_SU.value)
def set_superuser(message):
    usr = DB.getuserid(DB_BOT, TAB_LOG, str(message.chat.id))
    pas = setpasswd(usr[LOGI], message.text)
    save_state(id_bot=message.chat.id, pas=pas, st=ST.CHENGE_SU.value)
    usr = DB.getuserid(DB_BOT, TAB_LOG, str(message.chat.id))
    adm = {}
    adm['passw'] = usr[PAS]
    adm['ch_date'] = datetime.now().strftime("%Y-%m-%d %X")
    DB.updateonetask(DB_BOT, TAB_ROOT, usr[LOGI].lower(), adm)
    for i in list(DB.getonetask(DB_BOT, TAB_ROOT, usr[LOGI].lower()).items()):
        if i[0] == 'passw':
            bot.send_message(message.from_user.id, \
                '{}: {}'.format(NAME[i[0]], '**************'))
        else:
            bot.send_message(message.from_user.id, \
                '{}: {}'.format(NAME[i[0]], i[1]))
    user_markup = types.ReplyKeyboardMarkup(True, False)
    user_markup.row(app.config['MAIN_MENU'])
    user_markup.row(app.config['UPDATES'], app.config['FEEDBACK'])
    bot.send_message(message.from_user.id, app.config['SU_CHENGE'])
    bot.send_message(message.chat.id, app.config['SELECT_MENU'], \
        reply_markup=user_markup)
# ======================================================================
# ======================================================================

# ======================================================================
#============================= Flask ===================================
# Process webhook calls
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)


# Remove webhook, it fails sometimes the set if there is a previous webhook
bot.remove_webhook()
time.sleep(0.1)
# Set webhook
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                    certificate=open(WEBHOOK_SSL_CERT, 'r'))

if __name__ == '__main__':
    app.run(host=WEBHOOK_LISTEN,
            port=WEBHOOK_PORT,
            ssl_context=(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV),
            debug=True)

