from sqlalchemy import Column, DateTime, ForeignKey, BigInteger, String, func
from sqlalchemy.orm import backref, relationship
from sqlalchemy_cratedb.support import patch_autoincrement_timestamp

from database import Base

patch_autoincrement_timestamp()


class Department(Base):
    __tablename__ = "department"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String)


class Role(Base):
    __tablename__ = "roles"
    role_id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String)


class Employee(Base):
    __tablename__ = "employee"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String)
    # Use default=func.now() to set the default hiring time
    # of an Employee to be the current time when an
    # Employee record was created
    hired_on = Column(DateTime, default=func.now())
    department_id = Column(BigInteger, ForeignKey("department.id"))
    role_id = Column(BigInteger, ForeignKey("roles.role_id"))
    # Use cascade='delete,all' to propagate the deletion of a Department onto its Employees
    department = relationship(
        Department, backref=backref("employees", uselist=True, cascade="delete,all")
    )
    role = relationship(
        Role, backref=backref("roles", uselist=True, cascade="delete,all")
    )
