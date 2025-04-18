from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import task, user, auth


app = FastAPI()

# Allow frontend to make requests
origins = [
    "http://localhost:3000",  # Your frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.include_router(task.router)
app.include_router(user.router)
app.include_router(auth.router)
