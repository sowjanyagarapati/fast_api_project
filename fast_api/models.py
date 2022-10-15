from sqlalchemy import Column, Integer, String, Date, Float
from db import Base

class Customers(Base):
    """
    Defining Database Schema
    """
    __tablename__ = "customers"

    txn = Column(String)
    acc_number = Column(Integer)
    rrn = Column(Integer, primary_key=True, index=True)
    ifsc_number = Column(Integer)
    bank_name = Column(String)
    acc_holder_name = Column(String)
    txn_type = Column(String)
    TXN_DATE = Column(Date)
    AMOUNT = Column(Float)


