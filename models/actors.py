""" actors model for sqlalchemy """

from datetime import datetime
from sqlalchemy import Column, Text, String
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import BaseModel, Base
import json


class Actor(BaseModel, Base):
    '''
        defines an actor so we dont have to query for it again
    '''
    __tablename__ = "actors"
    actor_id = Column(String(13), nullable=False)
    actor_name = Column(String(41), nullable=False)
    stringJson = Column(Text, nullable=False)

    def __str__(self):
        return  "{}".format(json.loads(self.stringJson))
