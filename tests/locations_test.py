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
async def test_location_create(client: AsyncClient):
    response = await client.post('/locations/add',json=location1.dict())
    assert response.json() == db_location1
    assert response.status_code == 200
    response = await client.post('/locations/add',json=location2.dict())
    assert response.json() == db_location2
    assert response.status_code == 200
    
    
   
   


@mark.anyio
async def test_location_get_list(client: AsyncClient):
    response = await client.get('/locations/all')
    assert response.status_code == 200
    assert response.json() == [db_location1.dict(),db_location2.dict()]


@mark.anyio
async def  test_location_delete(client: AsyncClient):
    await client.post('/users/add', json=user1.dict())
    token = await client.post('/users/login', json=login_user1.dict())
    token = token.json()
    admin_response = await client.post("/users/add_admin?id=1", headers={'Token':token})
    assert admin_response.status_code == 200
    response = await client.delete('locations/delete?location_id=1&id=1',headers={'Token':token})
    assert response.status_code == 200
    assert response.json()['detail'] == 'Location with id 1 is successfully deleted'