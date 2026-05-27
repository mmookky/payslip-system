from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from auth import create_access_token, verify_password, get_current_employee
import models
import schemas

router = APIRouter(prefix="/employee", tags=["Employee"])


@router.post("/login")
def employee_login(data: schemas.EmployeeLogin, db: Session = Depends(get_db)):
    employee = db.query(models.Employee).filter(
        models.Employee.national_id == data.national_id
    ).first()
    if not employee or not verify_password(data.password, employee.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="เลขบัตรประชาชนหรือรหัสผ่านไม่ถูกต้อง"
        )
    token = create_access_token({"sub": employee.national_id, "role": "employee"})
    return {"access_token": token, "token_type": "bearer", "role": "employee"}


@router.get("/payslips", response_model=list[schemas.PayslipSummary])
def get_payslips(
    db: Session = Depends(get_db),
    current_employee: models.Employee = Depends(get_current_employee)
):
    return db.query(models.Payslip).filter(
        models.Payslip.employee_id == current_employee.id
    ).order_by(
        models.Payslip.year.desc(),
        models.Payslip.month.desc()
    ).all()


@router.get("/payslips/{payslip_id}", response_model=schemas.PayslipDetail)
def get_payslip_detail(
    payslip_id: int,
    db: Session = Depends(get_db),
    current_employee: models.Employee = Depends(get_current_employee)
):
    payslip = db.query(models.Payslip).filter(
        models.Payslip.id == payslip_id,
        models.Payslip.employee_id == current_employee.id
    ).first()

    if not payslip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ไม่พบข้อมูลสลิปเงินเดือน"
        )
    return payslip