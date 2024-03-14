from fastapi import FastAPI
from starlette import status

import models
from database import engine
from routers import auth, bets, events, users

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return {"is_healthy": True}


app.include_router(auth.router)
app.include_router(bets.router)
app.include_router(events.router)
app.include_router(users.router)
