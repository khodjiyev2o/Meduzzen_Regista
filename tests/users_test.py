from httpx import AsyncClient
from pytest import mark
from app.services.auth import AuthHandler
from schemas_mock import *

auth = AuthHandler()

@mark.anyio
async def test_healthcheck(client: AsyncClient, refresh_db):
    response = await client.get('/')
    assert response.status_code == 200
    assert response.json() == {'status': 'Working!'}


@mark.anyio
async def test_user_invalid_create(client: AsyncClient):
    invalid_user = dict(username='user', email='mail@mail.com', password1='password1', password2='password2')
    response = await client.post('/users/add', json=invalid_user)
    assert response.status_code == 422
    data = response.json()
    assert data['detail'][0]['msg'] == 'passwords do not match'

@mark.anyio
async def test_user_create(client: AsyncClient):
    response = await client.post('/users/add', json=user1.dict())
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == 1
    assert data['username'] == user1.username
    assert data['email'] == user1.email
    assert data['description'] == user1.description


@mark.anyio
async def test_user_double_create(client: AsyncClient):
    user = UserCreateSchema(username='user1', email='some@mail.com', password1='password', password2='password')
    response = await client.post('/users/add', json=user.dict())
    assert response.status_code == 404
    assert response.json() == {'detail': 'username or email already in use'}
    user = UserCreateSchema(username='some', email='mail1@mail.com', password1='password', password2='password')
    response = await client.post('/users/add', json=user.dict())
    assert response.status_code == 404
    assert response.json() == {'detail': 'username or email already in use'}


@mark.anyio
async def test_user_list(client: AsyncClient):
    response1 = await client.post('/users/add', json=user2.dict())
    print(response1.json())
    response2 = await client.post('/users/add', json=user3.dict())
    assert response1.status_code == 200
    assert response2.status_code == 200
    response = await client.get('/users/all')
    assert response.status_code == 200
    assert response.json() == [db_user1, db_user2, db_user3]


@mark.anyio
async def test_user_get(client: AsyncClient):
    response = await client.get('/users/1')
    assert response.status_code == 200
    assert response.json() == db_user1


@mark.anyio
async def test_user_login(client: AsyncClient):
    response = await client.post('/users/login', json=login_user1.dict())
    assert response.status_code == 200
    assert response.json() == auth.encode_token(email=user1.email)


@mark.anyio
async def test_user_invalid_login(client: AsyncClient):
    invalid_user = UserLoginSchema(email='some@mail.com', password='somepass')
    response = await client.post('/users/login', json=invalid_user.dict())
    assert response.status_code == 404
    assert response.json() == {'detail': 'user not found'}




@mark.anyio
async def test_user_validate_app(client: AsyncClient):
    user = UserAlterSchema(username='new_username', description='new one', password='new_pass')
    token = await client.post('/users/login', json=login_user1.dict())
    token = token.json()
    response = await client.patch('users/patch', headers={'Token': token}, json=user.dict())
    assert response.status_code == 200
    assert response.json() == UserSchema(id=1, username=user.username, email=user1.email, description=user.description).dict()
   
    




@mark.anyio
async def test_healthcheck_end(client: AsyncClient, clear_db):
    response = await client.get('/')
    assert response.status_code == 200
    assert response.json() == {'status': 'Working!'}
