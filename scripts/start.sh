echo '=========== RUNNING PIP INSTALL ==========='
python manage.py makemigrations

echo '===========  MAKING MIGRATIONS  ==========='
python manage.py migrate

echo '===========   RUNNING SERVER    ==========='
python manage.py runserver 0.0.0.0:4001
