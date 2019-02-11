## Flask Telegram Bot

Приложение реализовано с использованием [Flask](http://flask.pocoo.org/), библитеки [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) и базы данных [RethinkDB](https://www.rethinkdb.com/). Выбор [RethinkDB](https://ru.wikipedia.org/wiki/RethinkDB) обусловлен тем, что RethinkDB распределённая документоориентированная СУБД с открытым исходным кодом, сохраняющая данные в бессхемном JSON-формате. Ориентирована на применение для веб-приложений, требующих интенсивных обновлений базы данных.
В приложении используется метод [Webhook](https://tlgrm.ru/docs/bots/api#setwebhook), что позволяет получать одновления для бота с серверов Telegram.

Приложение позволяет выполнять регистрацию, аутентификацию, а также функции по изменению данных пользователя (смена пароля, смена данных введенных пользователем).

Функции api:
1. Регистрация нового пользователя;
2. Аутентификация пользователя;
3. Восстановление пароля пользователя;
4. Изменение данных пользователя:
    * ФИО
    * пол
    * пароль
    * номер телефона
    * email

Для работы с базой данных используется [диспетчер контекста](https://github.com/gwvsol/RethinkDB-context-manager).

Описание развертывания приложения опробовано на VDS c системой [CentOS7](https://www.centos.org/).

### Установка приложения
***
Установка Python3 и базы данных RethinkDB

```shell
yum -y install yum-utils
yum -y groupinstall development
# Устанавливаем репозиторий Python3
yum -y install https://centos7.iuscommunity.org/ius-release.rpm
# Устанавливаем Python3
yum -y install python36u
yum -y install python36u-devel
# Устанаваливаем пакетный менеджер pip
yum -y install python36u-pip
# Обновляем pip
pip3.6 install --upgrade pip

yum -y install wget
yum -y install screen
# Устанавливаем репозиторий для установки базы данных RethinkDB
wget http://download.rethinkdb.com/centos/7/`uname -m`/rethinkdb.repo -O /etc/yum.repos.d/rethinkdb.repo
# Устанавливаем базу данных RethinkDB
yum install rethinkdb
```

Загрузка проекта и создание виртуальной среды 
```shell
mkdir botapp
cd botapp
git clone https://github.com/gwvsol/Flask-Telegram-Bot.git ./
python3.6 -m venv venv
# Активируем виртуальную среду
source venv/bin/activate
# Обновляем pip3
pip3 install --upgrade pip
# Установливаем зависимости
pip3 install -r requirements.txt
```

[Настройка](https://www.rethinkdb.com/docs/start-on-startup/) базы данных RethinkDB
```shell
cp /etc/rethinkdb/default.conf.sample /etc/rethinkdb/instances.d/instance.conf
# Настраиваем базу данных
vim /etc/rethinkdb/instances.d/instance.conf
bind=127.0.0.1      #Работаем на localhost
driver-port=28015   #Порт на котором работает база данных
http-port=8080      #Порт Web интерфейса базы данных
# Настройка автозапуска базы данных
systemctl daemon-reload
systemctl enable rethinkdb

systemctl start rethinkdb   # Старт
systemctl status rethinkdb  # Проверка статуса работы БД
systemctl stop rethinkdb    # Стоп
systemctl restart rethinkdb # Рестарт
```

Настройка firewall
```shell 
firewall-cmd --permanent --add-port=8443/tcp # Порт на котором будет работать приложение
firewall-cmd --reload # Применяем настройки
```

Для работы приложения используются самоподписанных сертификаты. Создаем самоподписанный сертификат.

```shell
Cгенерируем приватный ключ
openssl genrsa -out webhook_pkey.pem 2048

Сгенерируем самоподписанный сертификат
openssl req -new -x509 -days 3650 -key webhook_pkey.pem -out webhook_cert.pem
ВАЖНО! Когда дойдем до Common Name (eg, your name or your server's hostname) []:
Следует указать IP адрес сервера или доменное имя сервера, на котором будет запущен бот.

```
Настраиваем Gunicorn

```shell

vim gunicorn.conf

bind = "0.0.0.0:8443" # Порт на котором будет работать приложение
# или через сокет
# bind = "unix:/home/proft/projects/blog/run/blog.socket"
#workers = 2
workers = 1
user = "work" # Имя пользователя от которого будет работать приложение
group = "work" # Группа пользователя от которого будет работать приложение
logfile = "/var/app_wsgi/bot/gunicorn.log"
loglevel = "info" #debug
proc_name = "bot"
pidfile = "/var/app_wsgi/bot/gunicorn.pid" # Пид файл
certfile = "webhook_cert.pem" # Сертификаты
keyfile = "webhook_pkey.pem"

```
Создать токен согласно документации [Telegram](https://core.telegram.org/bots/api)

Добавить полученный токен в файл ```config.py```
```shell
vim config.py
class Config(object):
# ====== debug mode ============
    DEBUG_MODE = True
# ===== Set Bot Telegram =======
    API_TOKEN = '742304158:AAFeunhPvTtDsgdgHJKHOIUHG1XU3iJPVNyBbTY'
```

```shell
Проверить работу приложения
screen gunicorn -c gunicorn.conf app:app

```
Если ошибок нет, настроить работу приложения через systemd.

```shell
cp flask-bot.service /usr/lib/systemd/system
vim /usr/lib/systemd/system/flask-bot.service

[Unit]
Description=uWSGI instance to serve flask-bot project
After=network.target

[Service]
User=work   # Здесь необходимо указать пользователя от которого будет выполняться приложение
Group=work  # Здесь необходимо указать группу пользователя от которого будет выполняться приложение
WorkingDirectory=/var/app_wsgi/bot              # Исправить пути к директории, где распологается приложение
Environment="PATH=/var/app_wsgi/bot/venv/bin"   # Исправить пути к директории, где распологается приложение
ExecStart=/var/app_wsgi/bot/venv/bin/gunicorn -c gunicorn.conf app:app # Исправить пути к директории, где распологается приложение

[Install]
WantedBy=multi-user.target

# Настройка автозапуска приложения
systemctl daemon-reload
systemctl enable flask-bot.service

systemctl start flask-bot.service     # Старт
systemctl status flask-bot.service    # Проверка статуса работы БД
systemctl stop flask-bot.service      # Стоп
systemctl restart flask-bot.service   # Рестарт

```

### Настройка приложения
***
Приложение имеет две команды ```start``` и ```setting```. Первая вводится при старте, вторая для настройки и входа в скрытое меню, где необходимо создать базу данных и пользователя администратора.
По умолчанию логин и пароль администратора root root. После создания нового администратора, дефолтная учетная запись будет отлючена. Если же база данных будет удалена, будет вновь активирована дефолтная учетная запись админитсратора, до тех пор пока не будет создана новая.

Используя меню приложения, можно создать новых пользователей и редактировать их учетные записи и просматривать их.
***



