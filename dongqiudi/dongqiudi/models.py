from sqlalchemy import Column, Integer, DateTime, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from .settings import MYSQL_DB

engine = create_engine(
    'mysql+mysqldb://{USER}:{PASSWORD}@{HOST}:{PORT}/dongqiudi?charset=utf8'.format(**MYSQL_DB['default']),
    poolclass=NullPool)
DBSession = sessionmaker(bind=engine)
Base = declarative_base()


class Articles(Base):
    __tablename__ = 'articles'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
    }

    id = Column(Integer(), primary_key=True)
    article_id = Column(Integer())
    label = Column(String(16))
    title = Column(String(64))
    writer = Column(String(32))
    body = Column(String(800))
    comments = Column(Integer())
    share = Column(Integer())
    tags = Column(String(64))
    source = Column(String(64))
    visit_total = Column(Integer())
    published_at = Column(DateTime)
    created_time = Column(DateTime)
    last_updated = Column(DateTime)


class URLStorage(Base):
    __tablename__ = 'url_storage'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }

    id = Column(Integer(), primary_key=True)
    url = Column(String(255))
