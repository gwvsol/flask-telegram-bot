# -*- coding: utf-8 -*-
from flask import Flask, request, abort
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
TAB_API = app.config['TAB_API']['data']
TAB_ROOT = app.config['TAB_BOT']['root']
#================================================


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


@bot.message_handler(func=lambda mess: app.config['MAIN_MENU'] == mess.text, content_types=['text'])
def main_menu(message):
    user_markup = types.ReplyKeyboardMarkup(True, False)
    user_markup.row(app.config['USER_DATA'])
    user_markup.row(app.config['CREATE_USER'], app.config['EDIT_PROFILE'])
    user_markup.row(app.config['SETTING'], app.config['PASSW_RECOV'])
    user_markup.row(app.config['UPDATES'], app.config['FEEDBACK']) 
    bot.send_message(message.from_user.id, app.config['SELECT_MENU'], reply_markup=user_markup) 
    

@bot.message_handler(func=lambda mess: app.config['USER_DATA'] == mess.text, content_types=['text'])
def main_menu(message):
    user_markup = types.ReplyKeyboardMarkup(True, False)
    user_markup.row(app.config['MAIN_MENU'])
    user_markup.row(app.config['UPDATES'], app.config['FEEDBACK'])
    bot.send_message(message.from_user.id, \
    app.config['LOGIN'], reply_markup=user_markup)
    

@bot.message_handler(func=lambda mess: app.config['CREATE_USER'] == mess.text, content_types=['text'])
def main_menu(message):
    user_markup = types.ReplyKeyboardMarkup(True, False)
    user_markup.row(app.config['MAIN_MENU'])
    user_markup.row(app.config['UPDATES'], app.config['FEEDBACK'])
    bot.send_message(message.from_user.id, \
    app.config['NEW_USER'], reply_markup=user_markup)


@bot.message_handler(func=lambda mess: app.config['EDIT_PROFILE'] == mess.text, content_types=['text'])
def main_menu(message):
    user_markup = types.ReplyKeyboardMarkup(True, False)
    user_markup.row(app.config['MAIN_MENU'])
    user_markup.row(app.config['UPDATES'], app.config['FEEDBACK'])
    bot.send_message(message.from_user.id, \
    app.config['LOGIN'], reply_markup=user_markup)


@bot.message_handler(func=lambda mess: app.config['PASSW_RECOV'] == mess.text, content_types=['text'])
def main_menu(message):
    user_markup = types.ReplyKeyboardMarkup(True, False)
    user_markup.row(app.config['MAIN_MENU'])
    user_markup.row(app.config['UPDATES'], app.config['FEEDBACK'])
    bot.send_message(message.from_user.id, \
    app.config['EMAIL'], reply_markup=user_markup)

#================= Меню Настройка приложения ================================
@bot.message_handler(func=lambda mess: app.config['SETTING'] == mess.text, content_types=['text'])
def main_menu(message):
    user_markup = types.ReplyKeyboardMarkup(True, False)
    user_markup.row(app.config['MAIN_MENU'])
    user_markup.row(app.config['UPDATES'], app.config['FEEDBACK'])
    bot.send_message(message.from_user.id, \
    app.config['LOGIN'], reply_markup=user_markup)

#================== О приложении, как связяться ========================
@bot.message_handler(func=lambda mess: app.config['UPDATES'] == mess.text, content_types=['text'])
def handle_text(message):
    user_markup = types.ReplyKeyboardMarkup(True, False)
    user_markup.row(app.config['MAIN_MENU'])
    bot.send_message(message.chat.id, \
    app.config['UPDATE'], reply_markup=user_markup)


@bot.message_handler(func=lambda mess: app.config['FEEDBACK'] == mess.text, content_types=['text'])
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

