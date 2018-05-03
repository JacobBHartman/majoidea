""" movies model for sqlalchemy """

from datetime import datetime
from sqlalchemy import Column, Text, String
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import BaseModel, Base
import json


class Movie(BaseModel, Base):
    '''
        defines an movie so we dont have to query for it again
    '''
    __tablename__ = "movies"
    movie_id = Column(String(13), nullable=False)
    stringJson = Column(Text, nullable=False)

    def __str__(self):
        return  "{}".format(json.loads(self.stringJson))

    @property
    def name(self):
        """
            Return name of movie
        """
        return stringJson["title"]


    @property
    def poster(self):
        """
            Return link to movie poster
        """
        return stringJson["poster"]["large"]
