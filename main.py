from fastapi import FastAPI
from routers import chat_router

app = FastAPI()
app.include_router(chat_router.router, tags=["Chat"])


@app.get("/")
def read_root():
    return {"message": "Hello from ai-sales-assistant-poc!"}
