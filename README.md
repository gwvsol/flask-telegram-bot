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





***



