from datetime import date, datetime

from sqlalchemy import create_engine, Table, Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

DATABASE_NAME = 'weight.sqlite'

engine = create_engine(f"sqlite+pysqlite:///{DATABASE_NAME}")
Session = sessionmaker()
session = Session(bind=engine)

Base = declarative_base()


def create_db():
    Base.metadata.create_all(engine)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    weights = relationship('Weight', lazy=True)

    def __repr__(self):
        return f'{self.id}'


class Weight(Base):
    __tablename__ = 'weighing'
    id = Column(Integer, primary_key=True)
    user = Column(ForeignKey('users.id'))
    weight = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now())

    def __repr__(self):
        return f'{self.weight}'


user = User()
session.add(user)
session.commit()

weight = Weight(weight=77.2)
session.add(weight)
session.commit()

users = session.query(User).all()
for user in users:
    print(user)


weights = session.query(Weight).all()
for weight in weights:
    print(weight.created_at)

user = session.query(User).filter(User.id == 1).first()
print(user)
weight = session.query(Weight).filter(Weight.id == 1).first()
print(weight)
user.weights.append(weight)
session.commit()
user = session.query(User).filter(User.id == 1).first()
print(user.weights)
for weight in user.weights:
    print(weight, 'kg', weight.created_at.strftime("%Y-%m-%d %H:%M"))
