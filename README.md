

Установка зависимостей: `pip install -r requirements.txt`.

Запуск: `python main.py` или `uvicorn main:app --reload`.
Документация API: http://127.0.0.1:8000/docs.

Подключение PostgreSQL настраивается в `.env` через `DATABASE_USER`,
`DATABASE_HOST`, `DATABASE_PASSWORD`, `DATABASE_NAME` и `DATABASE_PORT`.
База данных должна существовать; таблицы создаются автоматически при запуске.
PUT требует все поля пользователя. Пароли не возвращаются в ответах API.

Вход: POST /login/ с именем и паролем зарегистрированного пользователя.
Для постоянного ключа токенов задайте JWT_SECRET_KEY в .env; без него
после перезапуска нужно войти заново.
Изменять и удалять можно только свой аккаунт.
Для PUT и DELETE передайте заголовок X-CSRF-TOKEN со значением cookie
csrf_access_token, полученной при входе.


## Структура после переноса

```text
src/
  api/{auth.py,users.py}
  database/database.py
  database/models/{auth.py,user.py}
  schemas/{auth.py,user.py}
  core/{config.py,security.py,dependencies.py}
  main.py
tests/{test_auth.py,test_users.py}
alembic/versions/
.env.example
.gitignore
requirements.txt
main.py
```

Из корня проекта: `pip install -r requirements.txt`, скопировать `.env.example` в `.env`, заполнить настройки PostgreSQL, затем `uvicorn src.main:app --reload`. Старые команды `python main.py` и `uvicorn main:app --reload` также работают. Swagger: http://localhost:8000/docs.

Адреса API, схемы, хеширование, JWT-cookie и создание таблиц при запуске сохранены. Новых endpoints нет.

## Что дописать самостоятельно

- Написать тесты в tests/test_auth.py и tests/test_users.py: сейчас это пустые заготовки.
- Настроить Alembic и первую миграцию: сейчас подготовлены только каталоги; setup_db() оставлен.
- Исправить существующее несоответствие авторизации: register создаёт LoginModel без обязательного user_id, а login — без обязательного email. Вход ищет UserModel, регистрация сохраняет LoginModel. Это исходное поведение, перенос его не исправляет.
- При необходимости самостоятельно реализовать logout, current user, PATCH и смену пароля: в этом переносе они не добавлены.
