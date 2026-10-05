def test_register_user_creates_account_and_sets_cookie(client):
    payload = {
        "username": "alice",
        "email": "alice@example.com",
        "age": 22,
            "password": "StrongPass1",
    }

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 201
    assert response.json()["message"] == "Registration successful"
    assert response.cookies.get("access_token")


def test_login_accepts_registered_user(client):
    client.post(
        "/auth/register",
        json={
            "username": "bob",
            "email": "bob@example.com",
            "age": 22,
            "password": "StrongPass2",
        },
    )

    response = client.post(
        "/auth/login",
        json={"username": "bob", "age": 22,
            "password": "StrongPass2"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Login successful"
    assert response.cookies.get("access_token")


def test_user_list_requires_authentication(client):
    client.post(
        "/auth/register",
        json={
            "username": "charlie",
            "email": "charlie@example.com",
            "age": 22,
            "password": "StrongPass3",
        },
    )

    response = client.get("/users/")

    assert response.status_code == 200
    assert any(user["username"] == "charlie" for user in response.json())


def register(client, username='alice'):
    response = client.post('/auth/register', json={
        'username': username, 'email': f'{username}@example.com',
        'age': 23, 'password': 'StrongPass1',
    })
    assert response.status_code == 201
    return response.json()['user_id']


def csrf(client):
    return {'X-CSRF-TOKEN': client.cookies['csrf_access_token']}


def test_anonymous_access_is_rejected(client):
    assert client.get('/users/').status_code == 401


def test_update_delete_and_deleted_token(client):
    uid = register(client)
    response = client.put(f'/users/{uid}', headers=csrf(client), json={
        'username': 'updated', 'email': 'updated@example.com',
        'age': 30, 'password': 'UpdatedPass2',
    })
    assert response.status_code == 200
    assert response.json()['age'] == 30
    assert 'password' not in response.json()
    assert client.delete(f'/users/{uid}', headers=csrf(client)).status_code == 200
    assert client.get('/users/').status_code == 401


def test_foreign_account_changes_are_rejected(client):
    first = register(client, 'first')
    register(client, 'second')
    assert client.delete(f'/users/{first}', headers=csrf(client)).status_code == 403
    assert client.put(f'/users/{first}', headers=csrf(client), json={
        'username': 'changed', 'email': 'changed@example.com',
        'age': 30, 'password': 'UpdatedPass2',
    }).status_code == 403


def test_duplicate_and_missing_user(client):
    register(client)
    assert client.post('/auth/register', json={
        'username': 'alice', 'email': 'other@example.com',
        'age': 23, 'password': 'StrongPass1',
    }).status_code == 409
    assert client.get('/users/999999').status_code == 404


def test_csrf_is_required(client):
    uid = register(client)
    assert client.delete(f'/users/{uid}').status_code == 401
