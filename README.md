# API для групповых денежных сборов

[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=56C0C0&color=008080)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=56C0C0&color=008080)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat&logo=Django%20REST%20Framework&logoColor=56C0C0&color=008080)](https://www.django-rest-framework.org/)


## Описание проекта

Веб-сервис на базе Django, предоставляющий CRUD REST API для групповых денежных сборов.

Пользователь может создать групповой денежный сбор на выбор, например, свадьба, корпоратив, праздник и т.д. В нем он указывает название, повод, описание, сумму сбора (можно не указывать, чтобы сделать "бесконечный" сбор), обложку сбора, дату и время завершения.

Другие пользователи могут сделать пожертвования на любой сбор.

При создании группового денежного сбора или платежа по сбору на почту автора/
донатера придет письмо с информацией об успешном создании сбора (отправке платежа). 


## Запуск проекта локально

- Клонируйте репозиторий и перейдите в него в командной строке:
```
git clone git@github.com:cskovec22/CollectiveFundAPI.git
cd CollectiveFundAPI
```

- Установите и активируйте виртуальное окружение:

```
python -m venv venv
```

- Для Linux/macOS:

    ```
    source venv/bin/activate
    ```

- Для Windows:

    ```
    source venv/Scripts/activate
    ```

- Установите зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
pip install -r requirements.txt
```

- Создайте файл .env в папке проекта, пример представлен в файле .env.example  


- Перейдите в папку с файлом manage.py


- Примените миграции:
```
python manage.py makemigrations
python manage.py migrate
```

- Соберите статику:
```
python manage.py collectstatic
```

- Заполните базу данных командой:
```
python manage.py importdata
```

- Создайте суперпользователя:
```
python manage.py createsuperuser
```

- Запустите проект:
```
python manage.py runserver
```


## Список эндпоинтов API:

- /api/auth/users/ - список пользователей и их регистрация
- /api/auth/users/{id}/ - профиль пользователя
- /api/auth/users/me/ - текущий пользователь
- /api/auth/users/set_password/ - изменение пароля текущего пользователя
- /api/auth/token/login/ - получить токен авторизации
- /api/auth/token/logout/ - удалить токен текущего пользователя
- /api/v1/collects/ - список групповых денежных сборов
- /api/v1/collects/{id}/ - конкретный групповой денежный сбор
- /api/v1/payments/ - список донатов
- /api/v1/payments/{id}/ - конкретный донат


Подробную информацию по эндпоинтам API можно посмотреть по адресу:
```
http://localhost/api/docs/
```


### Автор:  
*Васин Никита*  
**email:** *cskovec22@yandex.ru*  
**telegram:** *@cskovec22*