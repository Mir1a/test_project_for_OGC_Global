from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Table, DateTime
from sqlalchemy.orm import relationship
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from ..database import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String)
    name = Column(String)
    last_name = Column(String, nullable=True)
    avatar = Column(String, nullable=True)
    born = Column(DateTime, nullable=True)
    hashed_password = Column(String(length=1024), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)


