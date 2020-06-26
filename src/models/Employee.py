from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Float
Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employee'

    employee_id = Column(Integer, primary_key=True, nullable=False)
    available_hrs = Column(Float, nullable=False)
    job_id = Column(Integer)
    status = Column(Boolean, nullable=False)
