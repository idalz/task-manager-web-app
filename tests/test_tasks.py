from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.main import app, get_db

# Set up a testing database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Recreate tables in test DB
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# Dependency override
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Use  TestClient to test fastAPI app
client = TestClient(app)

# Test POST /tasks/
def test_create_task():
    response = client.post("/tasks/", json={
        "title": "Test Task", 
        "description": "This is a test task"
    })
    assert response.status_code == 200
    data = response.json()
    assert data['title'] == "Test Task"
    assert data['description'] == "This is a test task"
    assert 'id' in data # Make sure task has an ID after creation

# Test GET /tasks/
def test_get_tasks():
    response = client.get("/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0 # Make sure there is at least one task

def test_get_task_by_id():
    # Create task
    task_data = {"title": "Task by ID", "description": "Fetch by ID"}
    create_response = client.post("/tasks/", json=task_data)
    task_id = create_response.json()["id"]

    # Fetch task by that id
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data['title'] == task_data['title']
    assert data['description'] == task_data['description']