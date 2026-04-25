from sqlalchemy import Column, String, Float, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid

Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"
    id = Column(String, primary_key=True)
    name = Column(String)
    email = Column(String)
    budget = Column(Float)
    preferences = Column(String)

engine = create_engine("sqlite:///./customer_agent/customers.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def save_customer(name: str, email: str, budget: float, preferences: str):
    db = SessionLocal()
    customer_id = str(uuid.uuid4())
    customer = Customer(id=customer_id, name=name, email=email, budget=budget, preferences=preferences)
    db.add(customer)
    db.commit()
    db.refresh(customer)
    db.close()
    return customer_id
