import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Sport(Base):
	__tablename__ = 'sport'
	name = Column(String(250), nullable=False)
	id = Column(Integer, primary_key=True)


class Item(Base):
	__tablename__ = 'item'
	name = Column(String(80), nullable=False)
	id = Column(Integer, primary_key=True)
	description = Column(String(250))
	sport_id = Column(Integer, ForeignKey('sport.id'))
	sport = relationship(Sport)

engine = create_engine('sqlite:///catalogitems.db')

Base.metadata.create_all(engine)