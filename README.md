# Веб-приложение для публикации постов «Blogicum»

## Описание проекта:

#### __Blogicum__  - сервис для публикации постов и комментариев к ним.

### Технологии:

-   Python 3.9
-   Django
-   SQLite
-   HTML
-   Pillow

### Возможности проекта:

-   регистрация пользователей
-   возможность добавления/редактирования/удаления своих публикаций
-   просмотр публикаций других пользователей
-   возможность добавления комментариев к публикациям
-   добавление к публикациям фото
-   просмотр публикаций в разрезе категорий и локаций

### Запуск проекта:_

-   Склонировать репозиторий:

```
git clone https://github.com/Spirual/blogicum.git

```

-   Создать и активировать виртуальное окружение:

```
python3 -m venv venv
source venv/bin/activate

```

-   Обновить pip:

```
python3 -m pip install --upgrade pip

```

-   Установить библиотеки:

```
pip install -r requirements.txt

```

-   Выполнить миграции:

```
python3 blogicum/manage.py migrate

```

-   Загрузить фикстуры DB:

```
python3 blogicum/manage.py loaddata db.json

```

-   Создать суперпользователя:

```
python3 blogicum/manage.py createsuperuser

```

-   Запустить сервер django:

```
python3 blogicum/manage.py runserver

```



Над проектом работал  [Владимир Фатеев](https://github.com/Spirual/).