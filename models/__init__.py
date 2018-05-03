'''
    Package initializer
'''

from models.engine import DBStorage
from models.base_model import Base
from models.searches import Search
from models.emails import Email
from models.movies import Movie
from models.actors import Actor


# creating db session
storage = DBStorage()
# creating db file and table if not alredy created
storage.reload()
