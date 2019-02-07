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
DB_API = app.config['DB_NAME']['db_api']
TAB_CHAT = app.config['TAB_BOT']['chat_log']
TAB_ROOT = app.config['TAB_BOT']['root']
TAB_API = app.config['TAB_API']['data']
ROOT_LOGIN = app.config['ROOT_USER']['login']
ROOT_PASSW = app.config['ROOT_USER']['passw']
USER = app.config['USER_PERMISS']
#USER[187911336] = '1'
DB = UseDB(DB_CONF)
ST = Status
#================================================
def save_user(i=None, l=None, p=None, st=None):
    if i:
        USER['id'] = i
        USER[i] = st
    if l:
        USER['login'] = l
    if p:
        USER['passw'] = p


def setpasswd(login: str, passw: str) -> str:
    """Преобразование пароля и логина в хеш MD5"""
    return str(md5(str(passw+login).lower().encode('utf-8')).hexdigest())
    
def verify(username=None, password=None):
    """Проверка пароля и логина"""
    i = 'id'
    p = 'passw'
    if username:
        if not password and DB.presence_id(DB_BOT, TAB_ROOT, i, username) == 1:
            return DB.presence_id(DB_BOT, TAB_ROOT, i, username)
        elif username and not password and username == ROOT_LOGIN:
            return ROOT_LOGIN
        else:
            return None
    elif password:
        if not username and DB.presence_id(DB_BOT, TAB_ROOT, p, password) == 1:
            return DB.presence_id(DB_BOT, TAB_ROOT, p, password)
        elif password and not username and setpasswd(USER['login'], password) == ROOT_PASSW:
            return ROOT_PASSW
        else:
            return None
    else:
        return None


#===================== Bot Telegram ====================================
@bot.message_handler(commands=['start'])
def handle_text(message):
    user_markup = types.ReplyKeyboardMarkup(True, False)
    user_markup.row(app.config['USER_DATA'])
    user_markup.row(app.config['CREATE_USER'], app.config['EDIT_PROFILE'])
    user_markup.row(app.config['SETTING'], app.config['PASSW_RECOV'])
    user_markup.row(app.config['UPDATES'], app.config['FEEDBACK'])
    bot.send_message(message.from_user.id, \
    app.config['SELECT_MENU'], reply_markup=user_markup)


@bot.message_handler(func=lambda message: app.config['MAIN_MENU'] == message.text, content_types=['text'])
def main_menu(message):
    user_markup = types.ReplyKeyboardMarkup(True, False)
    user_markup.row(app.config['USER_DATA'])
    user_markup.row(app.config['CREATE_USER'], app.config['EDIT_PROFILE'])
    user_markup.row(app.config['SETTING'], app.config['PASSW_RECOV'])
    user_markup.row(app.config['UPDATES'], app.config['FEEDBACK']) 
    bot.send_message(message.from_user.id, app.config['SELECT_MENU'], reply_markup=user_markup) 
    

@bot.message_handler(func=lambda message: app.config['USER_DATA'] == message.text, content_types=['text'])
def main_menu(message):
    user_markup = types.ReplyKeyboardMarkup(True, False)
    user_markup.row(app.config['MAIN_MENU'])
    user_markup.row(app.config['UPDATES'], app.config['FEEDBACK'])
    bot.send_message(message.from_user.id, \
        app.config['LOGIN'], reply_markup=user_markup)
    

@bot.message_handler(func=lambda message: app.config['CREATE_USER'] == message.text, content_types=['text'])
def main_menu(message):
    user_markup = types.ReplyKeyboardMarkup(True, False)
    user_markup.row(app.config['MAIN_MENU'])
    user_markup.row(app.config['UPDATES'], app.config['FEEDBACK'])
    bot.send_message(message.from_user.id, \
        app.config['NEW_USER'], reply_markup=user_markup)


@bot.message_handler(func=lambda message: app.config['EDIT_PROFILE'] == message.text, content_types=['text'])
def main_menu(message):
    user_markup = types.ReplyKeyboardMarkup(True, False)
    user_markup.row(app.config['MAIN_MENU'])
    user_markup.row(app.config['UPDATES'], app.config['FEEDBACK'])
    bot.send_message(message.from_user.id, \
        app.config['LOGIN'], reply_markup=user_markup)


@bot.message_handler(func=lambda message: app.config['PASSW_RECOV'] == message.text, content_types=['text'])
def main_menu(message):
    user_markup = types.ReplyKeyboardMarkup(True, False)
    user_markup.row(app.config['MAIN_MENU'])
    user_markup.row(app.config['UPDATES'], app.config['FEEDBACK'])
    bot.send_message(message.from_user.id, \
        app.config['EMAIL'], reply_markup=user_markup)

#================= Меню Настройка приложения ================================
@bot.message_handler(func=lambda message: app.config['SETTING'] == message.text, content_types=['text'])
def main_menu(message):
    user_markup = types.ReplyKeyboardMarkup(True, False)
    user_markup.row(app.config['MAIN_MENU'])
    user_markup.row(app.config['BASK_SET'])
    user_markup.row(app.config['UPDATES'], app.config['FEEDBACK'])
    save_user(i=message.chat.id, st=ST.LOGIN.value)
    bot.send_message(message.from_user.id, \
        app.config['LOGIN'], reply_markup=user_markup)

@bot.message_handler(func=lambda message: app.config['BASK_SET'] == message.text, content_types=['text'])
def main_menu(message):
    user_markup = types.ReplyKeyboardMarkup(True, False)
    user_markup.row(app.config['MAIN_MENU'])
    user_markup.row(app.config['BASK_SET'])
    user_markup.row(app.config['UPDATES'], app.config['FEEDBACK'])
    save_user(i=message.chat.id, st=ST.LOGIN.value)
    bot.send_message(message.from_user.id, \
        app.config['LOGIN'], reply_markup=user_markup)

@bot.message_handler(func=lambda message: USER[message.chat.id] == ST.LOGIN.value)
def user_entering_name(message):
    if verify(username=message.text) == message.text:
        save_user(i=message.chat.id, l=message.text, st=ST.PASSW.value)
        bot.send_message(message.chat.id, app.config['PASSW'])
    else:
        bot.send_message(message.chat.id, app.config['LOGIN_ERR'])
        return

@bot.message_handler(func=lambda message: USER[message.chat.id] == ST.PASSW.value)
def user_entering_passw(message):
    if verify(password=message.text) == setpasswd(USER['login'], message.text):
        passw = setpasswd(USER['login'], message.text)
        save_user(i=message.chat.id, l=message.text, p=passw, st=ST.CHECKED.value)
        bot.send_message(message.chat.id, app.config['PASSW_OK'])
        user_markup = types.ReplyKeyboardMarkup(True, False)
        user_markup.row(app.config['CREATE_DBASE'])
        bot.send_message(message.from_user.id, \
            app.config['SELECT_MENU'] + app.config['CREATE_DBASE'], reply_markup=user_markup)
    else:
        bot.send_message(message.chat.id, app.config['PASSW_ERR'])
        return


@bot.message_handler(func=lambda message: app.config['CREATE_DBASE'] == message.text, content_types=['text'])
def set_db(message):
    if USER[message.chat.id] == ST.CHECKED.value:
        user_markup = types.ReplyKeyboardMarkup(True, False)
        user_markup.row(app.config['CREATE_DB_TAB'])
        save_user(i=message.chat.id, st=ST.CHECKED.value)
        bot.send_message(message.from_user.id, \
            app.config['SELECT_MENU'] + app.config['CREATE_DB_TAB'], reply_markup=user_markup)
    else:
        user_markup = types.ReplyKeyboardMarkup(True, False)
        user_markup.row(app.config['MAIN_MENU'])
        user_markup.row(app.config['UPDATES'], app.config['FEEDBACK'])
        bot.send_message(message.chat.id, app.config['NO_ACCESS'] + app.config['CREATE_DBASE'])


@bot.message_handler(func=lambda message: app.config['CREATE_DB_TAB'] == message.text, content_types=['text'])
def set_tab(message):
    print(USER)
    print(app.config['USER_PERMISS'])
    if USER[message.chat.id] == ST.CHECKED.value:
        remove_markup = types.ReplyKeyboardRemove(True)
        save_user(i=message.chat.id, st=ST.SUPERUSER.value)
        bot.send_message(message.from_user.id, app.config['LOGIN_SUPERUSER'], reply_markup=remove_markup)
    else:
        user_markup = types.ReplyKeyboardMarkup(True, False)
        user_markup.row(app.config['MAIN_MENU'])
        user_markup.row(app.config['UPDATES'], app.config['FEEDBACK'])
        bot.send_message(message.chat.id, app.config['NO_ACCESS'] + app.config['CREATE_DB_TAB'], reply_markup=user_markup)


@bot.message_handler(func=lambda message: USER[message.chat.id] == ST.SUPERUSER.value)
def set_superuser(message):
    print(app.config['USER_PERMISS'])
    save_user(i=message.chat.id, l=message.text, st=ST.SUPER_PASS.value)
    print(USER)
    bot.send_message(message.from_user.id, app.config['PASSW_SUPERUSER'])


@bot.message_handler(func=lambda message: USER[message.chat.id] == ST.SUPER_PASS.value)
def set_superuser(message):
    save_user(i=message.chat.id, l=message.text, st=ST.START.value)
    print(USER)
    user_markup = types.ReplyKeyboardMarkup(True, False)
    user_markup.row(app.config['MAIN_MENU'])
    user_markup.row(app.config['UPDATES'], app.config['FEEDBACK'])
    bot.send_message(message.chat.id, app.config['FULL_SET'], reply_markup=user_markup)    


#================== О приложении, как связяться ========================
@bot.message_handler(func=lambda message: app.config['UPDATES'] == message.text, content_types=['text'])
def handle_text(message):
    user_markup = types.ReplyKeyboardMarkup(True, False)
    user_markup.row(app.config['MAIN_MENU'])
    bot.send_message(message.chat.id, \
    app.config['UPDATE'], reply_markup=user_markup)


@bot.message_handler(func=lambda message: app.config['FEEDBACK'] == message.text, content_types=['text'])
def handle_text(message):
    user_markup = types.ReplyKeyboardMarkup(True, False)
    user_markup.row(app.config['MAIN_MENU'])
    bot.send_message(message.chat.id, \
    app.config['QUESTIONS'], reply_markup=user_markup)


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

