from httpx import AsyncClient
from pytest import mark
from csv import writer, QUOTE_NONNUMERIC
from io import StringIO
from datetime import datetime
from schemas_mock import *
from app.services.auth import AuthHandler

auth = AuthHandler()

@mark.anyio
async def test_healthcheck(client: AsyncClient, refresh_db):
    response = await client.get('/')
    assert response.status_code == 200
    assert response.json() == {'status': 'Working!'}


@mark.anyio
async def test_worker_create(client: AsyncClient):
    await client.post('/users/add', json=user1.dict())
    await client.post('/users/add', json=user2.dict())
    await client.post('/users/add', json=user3.dict())
    response_location = await client.post('/locations/add',json=location1.dict())
    response_location.status_code == 200
    assert response_location.json() == db_location1
    token = await client.post('/users/login', json=login_user1.dict())
    token = token.json()
    admin_response = await client.post("/users/add_admin?id=1", headers={'Token':token})
    assert admin_response.status_code == 200
    response = await client.post('/workers/add', json=worker1.dict(), headers={'Token':token})
    assert response.json() == db_worker1
    assert response.status_code == 200
    
    
   
   


@mark.anyio
async def test_work_get_auth(client: AsyncClient):
    response = await client.get('/workers/all')
    assert response.status_code == 200
    assert response.json() == [db_worker1.dict()]


@mark.anyio
async def  test_worker_get_list(client: AsyncClient):
    token = await client.post('/users/login', json=login_user1.dict())
    token = token.json()
    response = await client.delete('workers/delete?worker_id=1&id=1',headers={'Token':token})
    assert response.status_code == 200
    assert response.json()['detail'] == 'Worker with id 1 is successfully deleted'