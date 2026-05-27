from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import get_db
from auth import create_access_token, verify_password, get_current_admin
import models
import schemas
import openpyxl
from io import BytesIO
from datetime import date

router = APIRouter(prefix="/admin", tags=["Admin"])

COLUMN_MAP = {
    "เลขรหัส / ID":                    "employee_code",
    "ชื่อ-สกุล / Name":                "full_name",
    "ID Card":                          "national_id",
    "แผนก / Department":               "department",
    "ตำแหน่ง / Position":              "position",
    "วันเริ่มทำงาน / Start Working":   "start_date",
    #
    "เงินเดือน / Salary":              "base_salary",
    "Paid Salary":                      "paid_salary",
    "Allowance":                        "allowance",
    "จำนวนชั่วโมงทำงานล่วงเวลา / Total Overtime": "overtime_hours",
    "สวัสดิการรวมทั้งหมด / Total Allowance":      "total_allowance",
    "รายการปรับ / Adjust":             "adjust",
    "Special":                          "special",
    "รายรับทั้งหมด / Total  Income":   "total_income",
    "รายการหัก /Deduct":               "deduct",
    "ประกันสังคม":                      "social_security",
    "TAX":                              "tax",
    "กองทุนสำรองเลี้ยงชีพ":           "provident_fund",
    "รวมรายการหัก":                    "total_deductions",
    "รวมทั้งหมด / Total Payment":      "net_pay",
    "รายได้สะสมประจำปี 2568":          "ytd_income",
    "ประกันสังคมสะสม ประจำปี 2568":   "ytd_sso",
    "Total TAX":                        "ytd_tax",
}


@router.post("/login")
def admin_login(data: schemas.AdminLogin, db: Session = Depends(get_db)):
    admin = db.query(models.Admin).filter(models.Admin.username == data.username).first()
    if not admin or not verify_password(data.password, admin.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง"
        )
    token = create_access_token({"sub": admin.username, "role": "admin"})
    return {"access_token": token, "token_type": "bearer", "role": "admin"}


@router.post("/upload", response_model=schemas.UploadResult)
def upload_payslip(
    month: int,
    year: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_admin: models.Admin = Depends(get_current_admin)
):
    # upload this month dup?
    existing = db.query(models.UploadHistory).filter_by(month=month, year=year).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"มีข้อมูลเดือน {month}/{year} อยู่แล้ว"
        )

    contents = file.file.read()
    wb = openpyxl.load_workbook(BytesIO(contents), read_only=True)
    ws = wb.active

    # read header row
    headers = []
    for cell in next(ws.iter_rows(min_row=1, max_row=1, values_only=True)):
        headers.append(str(cell).strip() if cell else "")

    # map header → index
    col_index = {}
    unknown_cols = []
    for i, h in enumerate(headers):
        if h in COLUMN_MAP:
            col_index[COLUMN_MAP[h]] = i
        elif h and h != "None":
            unknown_cols.append(h)

    errors = []
    if unknown_cols:
        errors.append(f"พบ column ที่ไม่รู้จัก (จะถูกข้าม): {', '.join(unknown_cols)}")

    # upload history
    upload = models.UploadHistory(
        admin_id=current_admin.id,
        filename=file.filename,
        month=month,
        year=year,
        status="processing"
    )
    db.add(upload)
    db.flush()

    total = success = failed = 0

    for row in ws.iter_rows(min_row=2, values_only=True):
        if not any(row):
            continue

        total += 1

        def get(field):
            idx = col_index.get(field)
            val = row[idx] if idx is not None else None
            if val == "" or val is None:
                return None
            return val

        national_id = str(get("national_id") or "").strip()
        if not national_id or national_id == "None":
            errors.append(f"แถว {total+1}: ไม่มีเลขบัตรประชาชน")
            failed += 1
            continue

        employee = db.query(models.Employee).filter_by(national_id=national_id).first()
        if not employee:
            full_name = str(get("full_name") or "").strip()
            parts = full_name.split(" ", 1)
            first_name = parts[0] if parts else full_name
            last_name = parts[1] if len(parts) > 1 else ""

            from auth import hash_password
            employee = models.Employee(
                national_id=national_id,
                employee_code=str(get("employee_code") or national_id),
                first_name=first_name,
                last_name=last_name,
                department=get("department"),
                position=get("position"),
                start_date=get("start_date"),
                password_hash=hash_password(national_id)
            )
            db.add(employee)
            db.flush()

        # check payslip dup?
        existing_slip = db.query(models.Payslip).filter_by(
            employee_id=employee.id, month=month, year=year
        ).first()
        if existing_slip:
            errors.append(f"แถว {total+1}: พนักงาน {national_id} มีข้อมูลเดือนนี้แล้ว")
            failed += 1
            continue

        try:
            payslip = models.Payslip(
                employee_id=employee.id,
                upload_id=upload.id,
                month=month,
                year=year,
                base_salary=get("base_salary") or 0,
                paid_salary=get("paid_salary") or 0,
                allowance=get("allowance") or 0,
                overtime_hours=get("overtime_hours") or 0,
                total_allowance=get("total_allowance") or 0,
                adjust=get("adjust") or 0,
                special=get("special") or 0,
                total_income=get("total_income") or 0,
                deduct=get("deduct") or 0,
                social_security=get("social_security") or 0,
                tax=get("tax") or 0,
                provident_fund=get("provident_fund") or 0,
                total_deductions=get("total_deductions") or 0,
                net_pay=get("net_pay") or 0,
                ytd_income=get("ytd_income") or 0,
                ytd_tax=get("ytd_tax") or 0,
                ytd_sso=get("ytd_sso") or 0,
            )
            db.add(payslip)
            db.flush()
            success += 1
        except Exception as e:
            errors.append(f"แถว {total+1}: {str(e)}")
            failed += 1

    upload.total_records = total
    upload.success_records = success
    upload.failed_records = failed
    upload.status = "completed"
    db.commit()

    return schemas.UploadResult(
        filename=file.filename,
        month=month,
        year=year,
        total_records=total,
        success_records=success,
        failed_records=failed,
        errors=errors
    )


@router.get("/uploads", response_model=list[schemas.UploadHistoryOut])
def get_upload_history(
    db: Session = Depends(get_db),
    current_admin: models.Admin = Depends(get_current_admin)
):
    return db.query(models.UploadHistory).order_by(
        models.UploadHistory.uploaded_at.desc()
    ).all()