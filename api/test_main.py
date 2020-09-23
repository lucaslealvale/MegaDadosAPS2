from fastapi.testclient import TestClient
from .main import app
import uuid

client = TestClient(app)


# Test 
def test_read_main_returns_not_found():
    response = client.get('/')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}
    

# Test read task list
def test_find_tasks():
    response = client.get('/task')
    assert response.status_code == 200

def test_find_completed_tasks():
    response = client.get('/task?completed=true')
    assert response.status_code == 200
    

def test_find_not_completed_tasks():
    response = client.get('/task?completed=false')
    assert response.status_code == 200

def test_find_not_completed_tasks_bool():
    response = client.get('/task?completed=batata')
    assert response.status_code == 422
    assert response.json() == {"detail":[{"loc":["query","completed"],"msg":"value could not be parsed to a boolean","type":"type_error.bool"}]}

# Test find specific test
def test_erro_find_task():
    response = client.get(f'/task/{uuid.uuid4()}')
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}

def test_erro_uuid_find_task():
    response = client.get('/task/biribiri')
    assert response.status_code == 422
    assert response.json() == {"detail":[{"loc":["path","uuid_"],"msg":"value is not a valid uuid","type":"type_error.uuid"}]}

def test_find_specific_task():
    res = client.post('/task', json={"description" : "alo alo 1 2 testando cambio", "completed" : False})
    uuid = res.json()
    response = client.get(f'/task/{uuid}')
    assert response.json() == {"description" : "alo alo 1 2 testando cambio", "completed" : False}
    

# Test create task   
def test_create_task():
    response = client.post('/task', json={ "description" : "alo alo 1 2 testando cambio", "completed" : False})
    assert response.status_code == 200


# Test replace task
def test_replace_task():
    res = client.post('/task', json={"description" : "alo alo 1 2 testando cambio", "completed" : False})
    uuid = res.json()
    response = client.put(f'/task/{uuid}',json={"description" : "1 2 3 pao tostado", "completed" : True})
    assert response.status_code == 200

def test_replace_nonexistent_task():
    response = client.put(f'/task/{uuid.uuid4()}',json={"description" : "1 2 3 pao tostado", "completed" : True})
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}

def test_replace_wrong_body_task():
    response = client.put(f'/task/batata',json={"description" : "1 2 3 pao tostado", "completed" : True})
    assert response.status_code == 422
    assert response.json() == {"detail":[{"loc":["path","uuid_"],"msg":"value is not a valid uuid","type":"type_error.uuid"}]}


# Test remove task
def test_remove_task():
    res = client.post('/task', json={"description" : "alo alo 1 2 testando cambio", "completed" : False})
    uuid = res.json()
    response = client.delete(f'/task/{uuid}')
    assert response.status_code == 200

def test_remove_nonexistent_task():
    response = client.delete(f'/task/{uuid.uuid4()}')
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}

def test_remove_nonexistent_task():
    response = client.delete('/task/batata')
    assert response.status_code == 422
    assert response.json() == {"detail":[{"loc":["path","uuid_"],"msg":"value is not a valid uuid","type":"type_error.uuid"}]}

# Test alter task 
def test_alter_task():
    res = client.post('/task', json={"description" : "alo alo 1 2 testando cambio", "completed" : False})
    uuid = res.json()
    response = client.patch(f'/task/{uuid}',json={"description" : "1 2 3 pao tostado", "completed" : False})
    assert response.status_code == 200

def test_alter_nonexistent_task():
    response = client.patch(f'/task/{uuid.uuid4()}',json={"description" : "1 2 3 pao tostado", "completed" : False})
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}

def test_alter_nonexistent_task():
    response = client.patch(f'/task/batata',json={"description" : "1 2 3 pao tostado", "completed" : False})
    assert response.status_code == 422
    assert response.json() == {"detail":[{"loc":["path","uuid_"],"msg":"value is not a valid uuid","type":"type_error.uuid"}]}