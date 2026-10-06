from sqlalchemy import create_engine
import os
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(url=DATABASE_URL)
sessionLocal = sessionmaker(bind=engine)
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally: 
        db.close()
        


