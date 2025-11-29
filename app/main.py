from fastapi import FastAPI
from app.core.config import settings
from app.routers import upload

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.get("/")
def health_check():
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME
    }

# --- Register Router ---
app.include_router(upload.router, prefix=settings.API_V1_STR + "/documents", tags=["Documents"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)