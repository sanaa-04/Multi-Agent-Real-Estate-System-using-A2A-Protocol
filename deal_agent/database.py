from sqlalchemy import Column, String, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid

Base = declarative_base()

class Property(Base):
    __tablename__ = "properties"
    id = Column(String, primary_key=True)
    address = Column(String)
    price = Column(Float)
    details = Column(String)

engine = create_engine("sqlite:///./deal_agent/deals.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def save_property(address: str, price: float, details: str):
    db = SessionLocal()
    property_id = str(uuid.uuid4())
    prop = Property(id=property_id, address=address, price=price, details=details)
    db.add(prop)
    db.commit()
    db.refresh(prop)
    db.close()
    return property_id
