

Установка зависимостей: `pip install -r requirements.txt`.

Запуск: `python main.py` или `uvicorn main:app --reload`.
Документация API: http://127.0.0.1:8000/docs.

Подключение PostgreSQL настраивается в `.env` через `DATABASE_USER`,
`DATABASE_HOST`, `DATABASE_PASSWORD`, `DATABASE_NAME` и `DATABASE_PORT`.
База данных должна существовать; таблицы создаются автоматически при запуске. PATCH обновляет переданные поля,
PUT требует все поля пользователя. Пароли не возвращаются в ответах API.
