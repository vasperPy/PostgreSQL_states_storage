# models.py
from sqlalchemy import Column, Integer, String, ARRAY, ForeignKey, PickleType, UniqueConstraint, JSON

from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    name = Column(String)
class Vids(Base):
    __tablename__ = 'vids'
    id = Column(Integer, primary_key=True)
    id_vids = Column(ARRAY(String), nullable=False)
class StateStorage(Base):
    __tablename__ = 'state_storage'
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String, unique=True, nullable=False)
    state = Column(String, nullable=True)
    data = Column(JSON, nullable=True)