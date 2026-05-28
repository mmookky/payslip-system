from sqlalchemy import Column, Integer, String, DateTime, Date, DECIMAL, ForeignKey, UniqueConstraint, LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Admin(Base):
    __tablename__ = "admins"

    id            = Column(Integer, primary_key=True, index=True)
    username      = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    email         = Column(String(100))
    created_at    = Column(DateTime, server_default=func.now())

    uploads = relationship("UploadHistory", back_populates="admin")


class Employee(Base):
    __tablename__ = "employees"

    id            = Column(Integer, primary_key=True, index=True)
    national_id   = Column(String(13), unique=True, nullable=False)
    employee_code = Column(String(20), unique=True, nullable=False)
    first_name    = Column(String(100), nullable=False)
    last_name     = Column(String(100), nullable=False)
    department    = Column(String(100))
    position      = Column(String(100))
    start_date    = Column(Date)
    password_hash = Column(String(255), nullable=False)
    created_at    = Column(DateTime, server_default=func.now())

    payslips = relationship("Payslip", back_populates="employee")


class UploadHistory(Base):
    __tablename__ = "upload_history"

    id              = Column(Integer, primary_key=True, index=True)
    admin_id        = Column(Integer, ForeignKey("admins.id"), nullable=False)
    filename        = Column(String(255), nullable=False)
    original_file   = Column(LargeBinary(length=2**24), nullable=True)
    error_file      = Column(LargeBinary(length=2**24), nullable=True)
    month           = Column(Integer, nullable=False)
    year            = Column(Integer, nullable=False)
    total_records   = Column(Integer, default=0)
    success_records = Column(Integer, default=0)
    failed_records  = Column(Integer, default=0)
    status          = Column(String(20), default="completed")
    uploaded_at     = Column(DateTime, server_default=func.now())

    admin    = relationship("Admin", back_populates="uploads")
    payslips = relationship("Payslip", back_populates="upload")

    __table_args__ = (
        UniqueConstraint("month", "year", "status", name="unique_upload_success"),
    )


class Payslip(Base):
    __tablename__ = "payslips"

    id               = Column(Integer, primary_key=True, index=True)
    employee_id      = Column(Integer, ForeignKey("employees.id"), nullable=False)
    upload_id        = Column(Integer, ForeignKey("upload_history.id"), nullable=False)
    month            = Column(Integer, nullable=False)
    year             = Column(Integer, nullable=False)

    base_salary      = Column(DECIMAL(12,2), default=0)
    paid_salary      = Column(DECIMAL(12,2), default=0)
    allowance        = Column(DECIMAL(12,2), default=0)
    overtime_hours   = Column(DECIMAL(8,2),  default=0)
    total_allowance  = Column(DECIMAL(12,2), default=0)
    adjust           = Column(DECIMAL(12,2), default=0)
    special          = Column(DECIMAL(12,2), default=0)
    total_income     = Column(DECIMAL(12,2), default=0)

    deduct           = Column(DECIMAL(12,2), default=0)
    social_security  = Column(DECIMAL(12,2), default=0)
    tax              = Column(DECIMAL(12,2), default=0)
    provident_fund   = Column(DECIMAL(12,2), default=0)
    tax_allowance    = Column(DECIMAL(12,2), default=0)
    welfare_fund     = Column(DECIMAL(12,2), default=0)
    total_deductions = Column(DECIMAL(12,2), default=0)

    net_pay          = Column(DECIMAL(12,2), default=0)

    ytd_income       = Column(DECIMAL(12,2), default=0)
    ytd_tax          = Column(DECIMAL(12,2), default=0)
    ytd_sso          = Column(DECIMAL(12,2), default=0)

    created_at       = Column(DateTime, server_default=func.now())

    employee = relationship("Employee", back_populates="payslips")
    upload   = relationship("UploadHistory", back_populates="payslips")

    __table_args__ = (
        UniqueConstraint("employee_id", "month", "year", name="unique_payslip"),
    )