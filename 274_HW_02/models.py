from requests import get
from bs4 import BeautifulSoup as BS
#import regex
import time

from sqlalchemy import Table, Column, ForeignKey,  Integer, String, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import sessionmaker
#from sqlalchemy import create_engine

Base = declarative_base()

assoc_post_tag = Table(
    'post_tag',
    Base.metadata,
    Column('blogpost', Integer, ForeignKey('blogpost.id')),
    Column('tag', Integer, ForeignKey('tag.id'))
)

#todo Class blog records
class BlogPost(Base):
    __tablename__ = 'blogpost'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    data = Column(String)
    url_bp = Column(String, unique=True)
    #tagl = Column(JSON)
    author_id = Column(Integer, ForeignKey('author.id'))
    writer_rel = relationship('Author', backref = 'blogposts')
    tags = relationship('Tag', secondary= assoc_post_tag, backref = 'blogposts')

    def __init__(self, title:str, data:str, url_bp : str,  writer_rel, tags = [] ):
        self.title = title
        self.data = data
        self.url_bp = url_bp
        self.writer_rel = writer_rel
        self.tags = tags
        #if tags:
         #   self.tags.extends(tags)
       # self.tagl = None


#todo Class for Tag
class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    url_t = Column(String, unique=True)
    def __init__(self, name: str, url_t:None):
        self.name = name
        self.url_t = url_t
 #   url_a = Column(String)
#


#todo Class for post author
class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name_a = Column(String)
    url_a = Column(String)

    def __init__(self, name_a:str, url_a:str ):
        self.name_a = name_a
        self.url_a = url_a





