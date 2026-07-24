from sqlalchemy import Column, Integer, String
# It is just a table design

from database import Base

class HospitalStaff(Base):

# class used to define structure of table

    __tablename__ = "HospitalStaff"

    id = Column(Integer, primary_key= True)

    username = Column(String)

    password = Column(String)

    role = Column(String)

    department = Column(String)

