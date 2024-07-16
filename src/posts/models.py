from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(1024))
    owner_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship("User")
