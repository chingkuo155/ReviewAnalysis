# main.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes import router as review_router
from fastapi.responses import HTMLResponse

app = FastAPI(title="Review Management System")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(review_router, prefix="/api", tags=["reviews"])

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()
    
# uvicorn main:app --reload