from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from decimal import Decimal


# ---- Auth ----

class AdminLogin(BaseModel):
    username: str
    password: str

class EmployeeLogin(BaseModel):
    national_id: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str


# ---- Employee ----

class EmployeeOut(BaseModel):
    id: int
    national_id: str
    employee_code: str
    first_name: str
    last_name: str
    department: Optional[str]
    position: Optional[str]
    start_date: Optional[date]

    class Config:
        from_attributes = True


# ---- Payslip ----

class PayslipSummary(BaseModel):
    id: int
    month: int
    year: int
    net_pay: Decimal

    class Config:
        from_attributes = True

class PayslipDetail(BaseModel):
    id: int
    month: int
    year: int

    base_salary: Decimal
    paid_salary: Decimal
    allowance: Decimal
    overtime_hours: Decimal
    total_allowance: Decimal
    adjust: Decimal
    special: Decimal
    total_income: Decimal

    deduct: Decimal
    social_security: Decimal
    tax: Decimal
    provident_fund: Decimal
    tax_allowance: Decimal
    welfare_fund: Decimal
    total_deductions: Decimal

    net_pay: Decimal

    ytd_income: Decimal
    ytd_tax: Decimal
    ytd_sso: Decimal

    employee: EmployeeOut

    class Config:
        from_attributes = True


# ---- Admin result ----

class AdminPayslipOut(BaseModel):
    id: int
    month: int
    year: int
    employee: EmployeeOut
    base_salary: Decimal
    paid_salary: Decimal
    total_income: Decimal
    total_deductions: Decimal
    net_pay: Decimal

    class Config:
        from_attributes = True


# ---- Upload ----

class UploadResult(BaseModel):
    id: int
    filename: str
    month: int
    year: int
    total_records: int
    success_records: int
    failed_records: int
    status: str
    has_error_file: bool
    errors: list[str]

class UploadHistoryOut(BaseModel):
    id: int
    filename: str
    month: int
    year: int
    total_records: int
    success_records: int
    failed_records: int
    status: str
    uploaded_at: datetime

    class Config:
        from_attributes = True