from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import model
from routes import auth
from database import engine


app = FastAPI()

model.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For development; restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)

@app.get("/")
def homePage():
    return {
        "message":"Welcome to QueryAnalyser"
    }