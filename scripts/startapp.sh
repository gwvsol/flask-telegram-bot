DIR="/app/bot"
cd $DIR
source venv/bin/activate
screen python3 app.py
#screen uwsgi --http-socket 0.0.0.0:5000 --manage-script-name --protocol=http --plugin pyththon3 -w app:app
