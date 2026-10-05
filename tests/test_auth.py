def test_register_and_login_work_for_a_new_user(client):
    register_response = client.post(
        "/auth/register",
        json={
            "username": "dana",
            "email": "dana@example.com",
            "age": 22,
            "password": "StrongPass4",
        },
    )
    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={"username": "dana", "age": 22,
            "password": "StrongPass4"},
    )

    assert login_response.status_code == 200
    assert login_response.json()["message"] == "Login successful"
    assert login_response.cookies.get("access_token")


def test_invalid_password_is_rejected(client):
    client.post('/auth/register', json={
        'username': 'alice', 'email': 'alice@example.com',
        'age': 24, 'password': 'StrongPass1',
    })
    assert client.post('/auth/login', json={
        'username': 'alice', 'password': 'WrongPass1',
    }).status_code == 401


def test_legacy_password_is_upgraded(client):
    import hashlib
    from sqlalchemy import select
    from src.database.database import new_session
    from src.database.models.user import UserModel
    client.post('/auth/register', json={
        'username': 'legacy', 'email': 'legacy@example.com',
        'age': 24, 'password': 'StrongPass1',
    })
    async def set_legacy():
        async with new_session() as session:
            user = await session.scalar(select(UserModel).where(UserModel.username == 'legacy'))
            user.password = hashlib.sha256(b'StrongPass1').hexdigest()
            await session.commit()
    client.portal.call(set_legacy)
    assert client.post('/auth/login', json={
        'username': 'legacy', 'password': 'StrongPass1',
    }).status_code == 200
    async def check_hash():
        async with new_session() as session:
            user = await session.scalar(select(UserModel).where(UserModel.username == 'legacy'))
            assert user.password.startswith('$argon2')
    client.portal.call(check_hash)
