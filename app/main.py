from fastapi import FastAPI

from app.presentation.api.routes.analysis_routes import router as analysis_router


app = FastAPI(
    title="Data Quality and Sentiment System",
    version="0.1.0"
)


@app.get("/")
def root():
    return {"message": "Data Quality and Sentiment System API"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(analysis_router)