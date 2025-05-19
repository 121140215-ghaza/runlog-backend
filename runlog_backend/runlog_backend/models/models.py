from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, Date
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(10), default='user')

    runlogs = relationship("RunLog", back_populates="user")
    goals = relationship("Goal", back_populates="user")

class RunLog(Base):
    __tablename__ = 'runlogs'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date = Column(Date, nullable=False)
    distance = Column(Float, nullable=False)
    duration = Column(Integer, nullable=False)
    note = Column(Text)

    user = relationship("User", back_populates="runlogs")

class Goal(Base):
    __tablename__ = 'goals'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    month = Column(String(7), nullable=False)  # Format: YYYY-MM
    target_distance = Column(Float, nullable=False)

    user = relationship("User", back_populates="goals")
