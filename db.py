from sqlalchemy import create_engine, DateTime, Text, ForeignKey, Float
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///blog.sqlite')

db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    nickname = Column(String(50))
    email = Column(String(120), unique=True)

    def __init__(self, first_name=None, last_name=None, email=None, nickname=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.nickname = nickname

    def __repr__(self):
        return '<User {}>'.format(self.nickname)


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    title = Column(String(140))
    image = Column(String(500))
    description = Column(String(500))


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    title = Column(String(140))
    image = Column(String(500))
    description = Column(String(500))
    price_usd = Column(Float(asdecimal=True))
    category_id = Column(Integer, ForeignKey('categories.id'))


class Photo(Base):
    __tablename__ = 'photos'
    id = Column(Integer, primary_key=True)
    photo = Column(String(500))
    product_id = Column(Integer, ForeignKey('products.id'))


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)

