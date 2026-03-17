from datetime import datetime
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db import Base, engine


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    wishlist = Column(String, nullable=False)  # вернуть unique=True

    telegram_id = Column(Integer)  # вернуть unique=True
    region = Column(String, nullable=False, index=True)
    registration_date = Column(DateTime, default=datetime.now)
    age = Column(Integer, nullable=True)

    games = relationship(
        'Game',
        secondary='user_game',
        back_populates='users',
        lazy='joined',
    )

    def __str__(self):
        return f'Пользователь {self.id} - {self.full_name} - {self.wishlist}'


class Game(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    url = Column(String, unique=True, nullable=False)
    original_price = Column(Float, nullable=False)
    actual_price = Column(Float, nullable=False)
    discount = Column(Float, nullable=True)
    igm_actual_price = Column(Float, nullable=True)
    igm_url = Column(String, unique=True, nullable=True)
    steambuy_actual_price = Column(Float, nullable=True)
    steambuy_url = Column(String, unique=True, nullable=True)

    users = relationship(
        'User',
        secondary='user_game',
        back_populates='games',
        lazy='joined',
    )

    def __repr__(self):
        return f'игра {self.id} - {self.name} - {self.url} - {self.price} - {self.actual_price} - {self.discount}'


class UserGame(Base):
    __tablename__ = 'user_game'
    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer,
        ForeignKey(User.id),
        index=True,
    )
    game_id = Column(
        Integer,
        ForeignKey(Game.id),
        index=True,
    )


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)



if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
