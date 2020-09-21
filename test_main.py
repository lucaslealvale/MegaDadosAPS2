from fastapi.testclient import TestClient
from main import app
import uuid

client = TestClient(app)

def test_read_main_returns_not_found():
    response = client.get('/')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}
    
def test_find_tasks():
    response = client.get('/task')
    assert response.status_code == 200
    assert response.json() == {}

def test_erro_find_task():
    response = client.get(f'/task/{uuid.uuid4()}')
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}

def test_create_task():
    response = client.post('/task', json={ "description" : "alo alo 1 2 testando cambio", "completed" : False})
    assert response.status_code == 200
    # assert type(response.json()) == str

def test_find_specific_task():
    res = client.post('/task', json={"description" : "alo alo 1 2 testando cambio", "completed" : False})
    uuid = res.json()
    response = client.get(f'/task/{uuid}')
    assert response.json() == {"description" : "alo alo 1 2 testando cambio", "completed" : False}

def test_replace_task():
    res = client.post('/task', json={"description" : "alo alo 1 2 testando cambio", "completed" : False})
    uuid = res.json()
    response = client.put(f'/task/{uuid}',json={"description" : "1 2 3 pao tostado", "completed" : True})
    assert response.status_code == 200

def test_replace_nonexistent_task():
    response = client.put(f'/task/{uuid.uuid4()}',json={"description" : "1 2 3 pao tostado", "completed" : True})
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}

def test_remove_task():
    res = client.post('/task', json={"description" : "alo alo 1 2 testando cambio", "completed" : False})
    uuid = res.json()
    response = client.delete(f'/task/{uuid}')
    assert response.status_code == 200

def test_remove_nonexistent_task():
    response = client.delete(f'/task/{uuid.uuid4()}')
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}

def test_alter_task():
    res = client.post('/task', json={"description" : "alo alo 1 2 testando cambio", "completed" : False})
    uuid = res.json()
    response = client.patch(f'/task/{uuid}',json={"description" : "1 2 3 pao tostado", "completed" : False})
    assert response.status_code == 200

def test_alter_nonexistent_task():
    response = client.patch(f'/task/{uuid.uuid4()}',json={"description" : "1 2 3 pao tostado", "completed" : False})
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}