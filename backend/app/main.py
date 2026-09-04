from fastapi import FastAPI
from app.analytics.opportunity import discover_cross_sell_opportunity
from app.agent import run_maya


app = FastAPI(
    title="MAYA API",
    description="Merchant Autonomous Yield Analyst",
    version="1.0.0"
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


@app.get("/api/opportunities")
def get_opportunity():
    return discover_cross_sell_opportunity()


@app.post("/api/maya/run")
def maya_run():
    return run_maya()