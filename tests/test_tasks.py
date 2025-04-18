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

    # Create a task
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "status": "pending",
        "due_date": "2025-04-30"
    } 
    response = client.post("/tasks/", json=task_data, headers=headers)

    assert response.status_code == 200
    data = response.json()

    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]
    assert data["status"] == task_data["status"]
    # Remove time in due_date for test
    assert data["due_date"].split("T")[0] == task_data["due_date"]
    assert 'id' in data # Make sure task has an ID after creation

# Test PUT /tasks/
def test_update_task(client):
    headers = register_and_login(client)

    # Create task
    create_data = {
        "title": "Original Task",
        "description": "Original Description",
        "status": "pending",
        "due_date": "2025-04-20"
    }
    response = client.post("/tasks/", json=create_data, headers=headers)
    task_id = response.json()["id"]

    # Update task
    update_data = {
        "title": "Updated Task",
        "description": "Updated Description",
        "status": "in-progress",
        "due_date": "2025-05-01"
    }

    update_response = client.put(f"/tasks/{task_id}", json=update_data, headers=headers)
    assert update_response.status_code == 200
    data = update_response.json()

    assert data["title"] == update_data["title"]
    assert data["description"] == update_data["description"]
    assert data["status"] == update_data["status"]
    # Remove time in due_date for test
    assert data["due_date"].split("T")[0] == update_data["due_date"]

# Test DELETE /tasks/
def test_delete_task(client):
    headers = register_and_login(client)

    # Create a task
    task_data = {
        "title": "Task",
        "description": "Task to delete",
        "status": "pending",
        "due_date": "2025-04-20"
    }
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
    task_data1 = {
        "title": "Task 1",
        "description": "Description",
        "status": "pending",
        "due_date": "2025-04-20"
    }
    client.post("/tasks/", json=task_data1, headers=headers)
    task_data2 = {
        "title": "Task 2",
        "description": "Description",
        "status": "pending",
        "due_date": "2025-04-20"
    }
    client.post("/tasks/", json=task_data2, headers=headers)
    
    # Get the tasks back
    response = client.get("/tasks/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0 # Make sure there is at least one task

def test_get_task_by_id(client):
    headers = register_and_login(client)

    # Create task
    task_data = {
        "title": "Task by id",
        "description": "Fetch by id",
        "status": "pending",
        "due_date": "2025-04-20"
    }
    create_response = client.post("/tasks/", json=task_data, headers=headers)
    task_id = create_response.json()["id"]

    # Fetch task by that id
    response = client.get(f"/tasks/{task_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data['title'] == task_data['title']
    assert data['description'] == task_data['description']
