def register_and_login(client):
    user_data = {
        "email": "testuser@example.com",
        "password": "testpassword"
    }

    # Register the user
    client.post("/users/register/", json=user_data)

    # Log in to get JWT token
    response = client.post("/login", data={
        "username": user_data["email"],
        "password": user_data["password"]
    })

    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

# Test POST /tasks/
def test_create_task(client):
    headers = register_and_login(client)

    response = client.post("/tasks/", json={
        "title": "Test Task", 
        "description": "This is a test task"
    }, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data['title'] == "Test Task"
    assert data['description'] == "This is a test task"
    assert 'id' in data # Make sure task has an ID after creation

# Test PUT /tasks/
def test_update_task(client):
    headers = register_and_login(client)

    # Create a task
    task_data = {"title": "Original Title", "description": "Original Description"}
    create_response = client.post("/tasks/", json=task_data, headers=headers)
    task_id = create_response.json()["id"]

    # Update the task
    updated_data = {"title": "Updated Title", "description": "Updated Description"}
    update_response = client.put(f"/tasks/{task_id}", json=updated_data, headers=headers)
    assert update_response.status_code == 200
    data = update_response.json()
    assert data['title'] == updated_data['title']
    assert data['description'] == updated_data['description']

# Test DELETE /tasks/
def test_delete_task(client):
    headers = register_and_login(client)

    # Create a task
    task_data = {"title": "Task to delete", "description": " Description to delete"}
    create_response = client.post("/tasks/", json=task_data, headers=headers)
    task_id = create_response.json()["id"]

    # Delete the  task
    delete_response = client.delete(f"/tasks/{task_id}", headers=headers)
    assert delete_response.status_code == 200
    deleted_task  = delete_response.json()
    assert deleted_task['id'] == task_id

    # Make sure it's deleted 
    get_response = client.get(f"/tasks/{task_id}", headers=headers)
    assert get_response.status_code == 404

# Test GET /tasks/
def test_get_tasks(client):
    headers = register_and_login(client)
     
    # Create tasks
    task_data = {"title": "Task 1", "description": "desc 2"}
    create_response = client.post("/tasks/", json=task_data, headers=headers)
    
    task_data = {"title": "Task 2", "description": "desc 2"}
    create_response = client.post("/tasks/", json=task_data, headers=headers)

    # Get the tasks back
    response = client.get("/tasks/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0 # Make sure there is at least one task

def test_get_task_by_id(client):
    headers = register_and_login(client)

    # Create task
    task_data = {"title": "Task by ID", "description": "Fetch by ID"}
    create_response = client.post("/tasks/", json=task_data, headers=headers)
    task_id = create_response.json()["id"]

    # Fetch task by that id
    response = client.get(f"/tasks/{task_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data['title'] == task_data['title']
    assert data['description'] == task_data['description']
