from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db import Base, engine


# nullable - поле может быть пустым
# unique - поле должно быть уникальным
# index - ускорение поиска по полю, но трата памяти

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    wishlist = Column(String, unique=True, nullable=False)
    telegram_id = Column(Integer, unique=True)
    region = Column(String, nullable=False, index=True)
    registration_date = Column(DateTime, default=datetime.now)

    games = relationship(
        'Game',
        secondary='user_game',
        back_populates='users',
        lazy='joined'
    )

    def __str__(self):
        return f'Пользователь {self.id} - {self.full_name} - {self.wishlist}'


class Game(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    url = Column(String, unique=True, nullable=False)
    price = Column(Integer, nullable=False)
    actual_price = Column(Integer, nullable=False)
    discount = Column(Integer, nullable=True)

    users = relationship(
        'User',
        secondary='user_game',
        back_populates='games',
        lazy='joined'
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

# id game_id user_id
# 1     7      12
# 2     5      12
# 3     2      6
# 4     7      11


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
