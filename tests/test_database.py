from sqlalchemy import text, inspect
from src.database.database import engine, setup_db


def test_missing_login_email_is_added_without_losing_history(client):
    async def check():
        async with engine.begin() as connection:
            await connection.execute(text('ALTER TABLE login DROP COLUMN email'))
            await connection.execute(text(
                "INSERT INTO users (id, username, age, email, password) "
                "VALUES (99, 'old', 20, 'old@example.com', 'oldhash')"
            ))
            await connection.execute(text(
                "INSERT INTO login (user_id, username, password) VALUES (99, 'old', '')"
            ))
        await setup_db()
        await setup_db()
        async with engine.connect() as connection:
            columns = await connection.run_sync(lambda sync: inspect(sync).get_columns('login'))
            assert 'email' in {column['name'] for column in columns}
            assert await connection.scalar(text('SELECT COUNT(*) FROM login WHERE user_id = 99')) == 1
    client.portal.call(check)
