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
    assert response.json() == {'status': 'Working from CI/CD GitHub actions by Samandar Khodjiyev for Meduzzen!'}


@mark.anyio
async def test_procedure_create(client: AsyncClient):
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
    response = await client.post('/workers/add', json=worker2.dict(), headers={'Token':token})
    assert response.json() == db_worker2
    assert response.status_code == 200

    response = await client.post('/procedures/add',json=procedure1.dict())
    assert response.json() == db_procedure1
    assert response.status_code == 200
    response = await client.post('/procedures/add',json=procedure2.dict())
    assert response.json() == db_procedure2
    assert response.status_code == 200
    
    
   
   


@mark.anyio
async def test_procedure_get_list(client: AsyncClient):
    response = await client.get('/procedures/all')
    assert response.status_code == 200
    assert response.json() == [db_procedure1.dict(),db_procedure2.dict()]


@mark.anyio
async def  test_procedure_delete(client: AsyncClient):
    token = await client.post('/users/login', json=login_user1.dict())
    token = token.json()
    response = await client.delete('procedures/delete?procedure_id=1&id=1',headers={'Token':token})
    assert response.status_code == 200
    assert response.json()['detail'] == 'Procedure with id 1 is successfully deleted'