""" DB storage engine """

from sqlalchemy import (create_engine)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlite3 import dbapi2 as sqlite
from models.searches import Search
from models.movies import Movie
from models.actors import Actor
from models.base_model import Base
from sqlalchemy import or_
import json


class DBStorage:
    """
        a connection for the database
    """
    __engine = None
    __session = None


    def __init__(self):
        """
            creating engine
        """
        self.__engine = create_engine(
        'sqlite+pysqlite:///majoidea.db', 
        native_datetime=True,
        module=sqlite, 
        pool_pre_ping=True, echo=False)

    def query_object(self, object):
        return [o for o in self.__session.query(object)]

    def query_searches(self, source_id, target_id):
        res = [o for o in self.__session.query(Search).filter(
            Search.source_actor_id == source_id,
            Search.target_actor_id == target_id
        )][0]
        if res:
            return res
        else:
            return None

    def query_actor(self, actor_id="", actor_name=""):
        res = [o.stringJson for o in self.__session.query(Actor).filter(or_(
            Actor.actor_id == actor_id,
            Actor.actor_name == actor_name))]
        try:
            res = res[0]
        except:
            return None
        if res:
            return json.loads(res)
        else:
            return None
    
    def query_movie(self, movie_id):
        res = [o.stringJson for o in self.__session.query(Movie).filter(Movie.movie_id == movie_id)]
        try:
            res = res[0]
        except:
            return None
        if res:
            return json.loads(res)
        else:
            return None

    def new(self, obj):
        """
            adding new obj to session queue
        """
        self.__session.add(obj)

    def save(self):
        """
            commiting session queue and database
        """
        self.__session.commit()


    def reload(self):
        """
            reload is in charge of creating table if
            it hasent been created and is also responsible
            for creating the session from the engine
            it is set to not expire on commit 
            so it stays connected through out 
            the apps life cylce
        """
        Base.metadata.create_all(self.__engine)
        sesh_maker = sessionmaker(
            bind=self.__engine,
            expire_on_commit=False)
        self.__session = scoped_session(sesh_maker)

    def close(self):
        '''
        Calls remove method on the private session attribute or
        close method on the class Session
        '''
        self.__session.close()
