from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.agent import run_maya


app = FastAPI(
    title="MAYA API",
    description="Merchant Autonomous Yield Analyst",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "product": "MAYA",
        "status": "online"
    }


@app.get("/api/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/api/maya/run")
def maya_run():
    return run_maya()