## Restful Api on Flask

Приложение реализовано с использованием [Flask](http://flask.pocoo.org/) и базы данных [RethinkDB](https://www.rethinkdb.com/). Выбор [RethinkDB](https://ru.wikipedia.org/wiki/RethinkDB) обусловлен тем, что RethinkDB распределённая документоориентированная СУБД с открытым исходным кодом, сохраняющая данные в бессхемном JSON-формате. Ориентирована на применение для веб-приложений, требующих интенсивных обновлений базы данных.

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

Для работы с базой данных используется [диспетчер контекста](https://github.com/gwvsol/RethinkDB-context-manager) разработанный для данного приложения.

Приложение сделано очень разговорчивым, т.е на все действия пользователей будет дан ответ или о положительном выполнении операции или о причине неудачи. Что дает возможность понять что происходит с приложением и тем самым достигается результат логирования приложения.

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
# Устанавливаем репозиторий для установки базы данных RethinkDB
wget http://download.rethinkdb.com/centos/7/`uname -m`/rethinkdb.repo -O /etc/yum.repos.d/rethinkdb.repo
# Устанавливаем базу данных RethinkDB
yum install rethinkdb
```
Загрузка проекта и создание виртуальной среды 
```shell
mkdir webapp
cd webapp
git clone https://github.com/gwvsol/Restful-Api-on-Flask.git ./
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
#firewall-cmd --permanent --add-port=8080/tcp 
firewall-cmd --permanent --add-port=5000/tcp # Порт на котором будет работать приложение
firewall-cmd --reload # Применяем настройки
```

Подготовка к запуску приложения
```shell
vim uwsgi.ini
uid = work # Здесь необходимо указать пользователя от которого будет выполняться приложение
gid = work # Здесь необходимо указать группу пользователя от которого будет выполняться приложение
#Проверить работу приложения можно таким образом
uwsgi --ini uwsgi.ini
#Настройка работы приложения через systemd
cp flask-uwsgi.service /usr/lib/systemd/system
vim /usr/lib/systemd/system/flask-uwsgi.service
[Service]
User=work   # Здесь необходимо указать пользователя от которого будет выполняться приложение
Group=work  # Здесь необходимо указать группу пользователя от которого будет выполняться приложение
WorkingDirectory=/var/app_wsgi/wsgi            # Исправить пути к директории, где распологается приложение
Environment="PATH=/var/app_wsgi/wsgi/venv/bin" # Исправить пути к директории, где распологается приложение
ExecStart=/var/app_wsgi/wsgi/venv/bin/uwsgi --ini uwsgi.ini # Исправить пути к директории, где распологается приложение
# Настройка автозапуска приложения
systemctl daemon-reload
systemctl enable flask-uwsgi.service

systemctl start flask-uwsgi.service     # Старт
systemctl status flask-uwsgi.service    # Проверка статуса работы БД
systemctl stop flask-uwsgi.service      # Стоп
systemctl restart flask-uwsgi.service   # Рестарт
```
### Настройка приложения
***

По умолчанию логин и пароль доступа к приложению установлен ```root:root```

Если необходимо изменить логин и пароль по умолчанию:
```python
from hashlib import md5
def setpasswd(login: str, passw: str) -> str:
    """Преобразование пароля и логина в хеш MD5"""
    return str(md5(str(passw+login).lower().encode('utf-8')).hexdigest())
```
После чего измените соответствующие поля в файле ```config.py```

Все настройки приложения (название базы данных, названия таблиц, ```help```), даны в файле ```config.py```.

#### Промотр существуюзих баз даных: *http://IP:5000/api/db*

```curl -s -u root:root -G http://IP:5000/api/db```

Для более красивого выводы можно использовать приложение ```jq```, в таком случае запрос к приложению будет следующим:

```curl -s -u root:root -G http://IP:5000/api/db | jq '.'```

#### Создание новой базы данных ```data``` для работы приложения: *http://IP:5000/api/db*

```curl -s -u root:root -X POST http://IP:5000/api/db```

```для удаления базы данных используется запрос DELETE```

#### Создание таблиц ```data```, ```log```, ```root```, для работы приложения: *http://IP:5000/api/tab*

```curl -s -u root:root -X POST http://IP:5000/api/tab```

```для просмотра существующих таблиц используется запрос GET, удаления всех таблиц запрос DELETE```

#### Создание суперпользователя и отключение дефолтной учетной записи root:

Для упрощения процедуры необходимо использовать скрпт [```root_user.sh```](https://github.com/gwvsol/Restful-Api-on-Flask/blob/master/scripts/root_user.sh), измените в нем:

```shell
remoteHost="uwsgi.loc:5000"
login="admin"
passw="admin"
```
после чего сделайте файл исполняемым и запустите его. 

Создание нового суперпользователя автоматически отключает дефолтную учетную запись ```root:root```. Все дальнейшие запросы к приложению должны быть выполнены от нового супепользователя. Изменить ```login``` нового суперпользователя нельзя. Можно изменить его пароль используя ```root_user.sh```. Если же необходимо изменить ```login``` суперпользователя, необходимо используя запрос ```DELETE``` удалить запись полностью, и использую дефолтный ```login: passwd``` создать новую учетную запись суперпользователя. При удалении учетной записи суперпользователя, автоматически разблокируется делолтный ```login: passwd```. Просмотр данных суперпользователя выполняется запросом ```GET```.

#### Просмотр суперпользователем всех записей пользователей: *http://IP:5000/api/all*

Суперпользователь имеет возможность просмотреть все записи пользователей в базе данных. Для этого используется запрос ```GET```.

```curl -s -u root:root -G http://IP:5000/api/all```

#### Создание нового пользователя и просмотр справки ```help```: *http://IP:5000/api/new*

При использовании запроса ```GET```

```curl -s -G http://IP:5000/api/new```

выводится справка по созданию нового пользователя, редактирования данных пользователя и восстановления пароля

При использовании запроса ```POST``` и передаче данных в формате ```JSON``` в виде:
```curl -s -H Content-Type: application/json -X POST -d "YOUR DATA" http://IP:5000/api/new```
```json
{
    "email": "mail@mail.ru",
    "gender": "male",
    "login": "data",
    "name": "Busan",
    "passw": "dsfsdfsdaf",
    "phone": "79005006826"
}
```
происходит создание нового пользователя.
Для упрощения тестирования приложения можно использовать скрипт [```user.sh```](https://github.com/gwvsol/Restful-Api-on-Flask/blob/master/scripts/user.sh). 

#### Запросы пользователей, редактирование профиля и его удаление: *http://IP:5000/api/user/login*
Запрос ```GET```: вывод всей информации о пользователе. Пароль выводится в виде xеша.

```curl -s -u data:data -G  https://api.hldns.ru/api/user/data```

Запрос ```POST``` редактирование данных профиля. Запрос формируется аналогичным способом как при создании нового пользователя плюс данные для аутентификации пользователя. При редактировании ```login``` пользователя изменить не возможно. Для упрощения тестирования, можно использовать скрипт [```update_user.sh```](https://github.com/gwvsol/Restful-Api-on-Flask/blob/master/scripts/update_user.sh).

```curl -s -u data:data -H Content-Type: application/json -X POST -d "YOUR DATA" http://IP:5000/api/user/login```
```json
{
    "email": "mail@mail.ru",
    "gender": "male",
    "name": "Busan",
    "passw": "dsfsdfsdaf",
    "phone": "79005006826"
}
```
Использование запроса ```DELETE``` приводит к удалению пользователя.

```curl -s -u data:data -X DELETE  https://api.hldns.ru/api/user/data```

#### Восстановление пароля пользователя: *http://IP:5000/api/passw/login*

Запрос ```POST```: восстановление пароля. Для восстановления необходимо передать в формате ```JSON``` данные для восстановления пароля.

```curl -s -u data:data -H Content-Type: application/json -X POST -d "YOUR DATA" http://IP:5000/api/passw/login```
```json
{
    "email": "mail@mail.ru",
    "passw": "dsfsdfsdaf",
    "phone": "79005006826"
}
```
Для тестирования приложения можно использовать скрипт [```user_passw.sh```](https://github.com/gwvsol/Restful-Api-on-Flask/blob/master/scripts/user_passw.sh)
***



