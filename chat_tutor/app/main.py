from fastapi import FastAPI
from .router import router
from .deps import limiter

app = FastAPI(title="ChatTutor API", description="Lightweight AI tutoring service")

app.include_router(router)

@app.get("/")
async def root():
    return {"app":"ChatTutor"}