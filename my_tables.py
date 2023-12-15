from sqlalchemy import  Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base




Base = declarative_base()


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    item_name = Column(String)
    item_quantity = Column(Integer)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    customer = relationship('Customer', back_populates='orders')

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, autoincrement=True) 
    name = Column(String)
    location = Column(String)
    email = Column(String)
    orders = relationship('Order', back_populates='customer')


