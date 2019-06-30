import sys

from sqlalchemy import Column, Numeric, String, Integer, ForeignKey, create_engine

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Restaurant(Base):
    __tablename__ = 'restaurant'
    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)

class MenuItem(Base):
    __tablename__ = 'menu_item'
    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    description = Column(String(280))
    course = Column(String(10))
    price = Column(String(6), nullable = False)
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

    @property
    def serialize(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'course' : self.course,
            'description' : self.description,
            'price' : self.price,
        }

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)
