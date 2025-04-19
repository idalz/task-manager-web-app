import httpx
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.requests import Request
from app.routes import task, user, auth
from app.models.user import User
from app.dependencies.auth import get_current_user
from app.database import get_db
from sqlalchemy.orm import Session
from app.dependencies.auth import oauth2_scheme

app = FastAPI()

# CORS middleware for handling cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup for static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Setup for Jinja2 template rendering
templates = Jinja2Templates(directory="app/templates")

# Include routers for tasks, users, and authentication
app.include_router(task.router)
app.include_router(user.router)
app.include_router(auth.router)

# Root route that redirects to the login page
@app.get("/", response_class=RedirectResponse)
async def root():
    return RedirectResponse(url="/login")

# Login page 
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Register page
@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})
