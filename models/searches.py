""" searches model for sqlalchemy """

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import BaseModel, Base
import json



class Search(BaseModel, Base):
    '''
        defines a previous searches so that we don't querry api for 
        repetitive searches
    '''
    __tablename__ = "searches"
    source_actor_name = Column(String(41), nullable=False)
    target_actor_name = Column(String(41), nullable=False)
    stringJson = Column(Text, nullable=False)

    def __str__(self):
        return  "{}".format(json.loads(self.stringJson))
