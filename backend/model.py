from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String 

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[String]=mapped_column(String(100), nullable=False)
    email:Mapped[String]=mapped_column(String(100), nullable=False, unique=True)
    password:Mapped[String]=mapped_column(String(100))