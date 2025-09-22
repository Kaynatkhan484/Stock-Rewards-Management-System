# Stocky API

Version: 0.1.0  
Framework: FastAPI  
Database: PostgreSQL  

## Features

- Manage Users and Rewards
- CRUD endpoints for rewards and users
- View stats, portfolio, today’s stocks, historical INR

## How to Run

1. Clone repo  
2. Create virtual environment: `python -m venv venv`  
3. Activate venv: `.\venv\Scripts\Activate.ps1`  
4. Install dependencies: `pip install -r requirements.txt`  
5. Run server: `uvicorn stocky.api.main:app --reload`  
6. Open browser: `http://127.0.0.1:8000/docs` for Swagger UI
