import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(45), nullable=False)
    picture = Column(String(512))


class Sport(Base):
    __tablename__ = 'sport'
    name = Column(String(250), nullable=False)
    id = Column(Integer, primary_key=True)
    picture = Column(String(512))
    item = relationship(Item, cascade="delete")

    @property
    def serialize(self):
        # Returns object data in easily serializable format
        return {
            'name': self.name,
            'id': self.id,
            'picture': self.picture,
        }


class Item(Base):
    __tablename__ = 'item'
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    sport_id = Column(Integer, ForeignKey('sport.id'))
    sport = relationship(Sport)
    picture = Column(String(512))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        # Returns object data in easily serializable format
        return {
            'name': self.name,
            'id': self.id,
            'description': self.description,
            'picture': self.picture,
        }
engine = create_engine('sqlite:///catalogitems.db')

Base.metadata.create_all(engine)
