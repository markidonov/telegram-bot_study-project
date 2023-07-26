# telegram-bot_study-project
study-project

Телеграм-бот с использованием Django и python-telegram-bot
с возможностями администрирования через стандартную админку 
и дополнительный веб-сервис.

## Документация по проекту

Для запуска проекта необходимо

#### Установить зависимости:

```bash
pip install -r requirements.txt
```

#### Провести миграцию:

```bash
python manage.py migrate
```

#### Создать суперпользователя

```bash
 python manage.py createsuperuser
```


#### Запустить вместе либо по-отдельности веб-сервер и бота :

```bash
 python manage.py runserver | python manage.py bot
```