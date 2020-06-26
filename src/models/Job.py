from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Float
Base = declarative_base()

class Job(Base):
    __tablename__ = 'job'

    job_id = Column(Integer, primary_key=True, nullable=False)
    job_desc = Column(String(100))
    hrs_required = Column(Float, nullable=False)
    assignee = Column(String(100))
    status = Column(Boolean, nullable=False)
