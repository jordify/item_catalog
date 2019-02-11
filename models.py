import random, string

from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey, create_engine, func
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
)

Base = declarative_base()
secret_key = ''.join(random.SystemRandom().choice(string.ascii_uppercase \
    + string.digits) for x in range(32))

class Category(Base):
  __tablename__ = 'category'

  id = Column(Integer, primary_key=True)
  name = Column(String(80), nullable=False)

  @property
  def serialize(self):
    return {
        'name': self.name,
        'id': self.id
    }

class Item(Base):
  __tablename__ = 'item'

  id = Column(Integer, primary_key=True)
  name = Column(String(80), nullable=False)
  description = Column(String(500))
  time_created = Column(DateTime, server_default=func.now())
  time_updated = Column(DateTime, onupdate=func.now())
  category_id = Column(Integer, ForeignKey('category.id'))
  category = relationship(Category)

  @property
  def serialize(self):
    return {
        'name': self.name,
        'id': self.id,
        'description': self.description,
        'time_created': self.time_created,
        'time_updated': self.time_updated,
        'category_id': self.category_id
    }


class User(Base):
  __tablename__ = 'user'

  id = Column(Integer, primary_key=True)
  username = Column(String(32))
  email = Column(String(200))
  pwd_hash = Column(String(64))

  def hash_password(self, password):
    self.pwd_hash = pwd_context.encrypt(password)
    return True

  def verify_password(self, password):
    return pwd_context.verify(password, self.pwd_hash)

  def generate_auth_token(self, expiration=600):
    s = Serializer(secret_key, expires_in = expiration)
    return s.dumps({'id': self.id })

  @staticmethod
  def verify_auth_token(token):
    s = Serializer(secret_key)
    try:
      data = s.loads(token)
    except SignatureExpired:
      return (False, 'Expired')
    except BadSignature:
      return (False, 'Bad')
    user_id = data['id']
    return (True, user_id)

  @property
  def serialize(self):
    return {
        'username': self.username,
        'id': self.id,
        'email': self.email
    }
engine = create_engine('sqlite:///catalog.db')

Base.metadata.create_all(engine)
