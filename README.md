# Self-Service Payslip System

ระบบ Self-Service สำหรับดูเอกสารเงินเดือนของพนักงาน โดย HR/Admin สามารถ Upload ข้อมูลเงินเดือนจากไฟล์ Excel และพนักงานสามารถ Login เพื่อดูข้อมูลเงินเดือนของตนเองในแต่ละเดือนได้

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Nuxt 3, Vue 3, Vuetify 3 |
| Backend | Python 3.11, FastAPI |
| Database | MySQL 8.0 |
| DevOps | Docker, Docker Compose |

---

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Git](https://git-scm.com/)
- Node.js 20+ (สำหรับ local development เท่านั้น)

---

## Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/payslip-system.git
cd payslip-system
```

### 2. Setup Environment Variables

```bash
cp .env.txt .env
```

แก้ไขค่าใน `.env` ตามต้องการ:

```env
DB_ROOT_PASSWORD=rootpassword123
DB_NAME=payslip_db
DB_USER=payslip_user
DB_PASSWORD=payslip_pass123
SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
```

### 3. Setup Frontend Environment

```bash
cp frontend/.env.txt frontend/.env
```

ค่าใน `frontend/.env`:

```env
NUXT_PUBLIC_API_BASE=http://localhost:8000
```

### 4. Run with Docker

```bash
docker compose up -d --build
```

รอประมาณ 1-2 นาที แล้วเปิด browser:

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |

---

## Running Frontend & Backend Separately (Local Development)

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## Database Setup

Database จะถูกสร้างอัตโนมัติเมื่อรัน Docker ครั้งแรก จาก `database/init.sql`

หากต้องการ reset database:

```bash
docker compose down -v
docker compose up -d --build
```

### Connect with DBeaver

```
Host:     localhost
Port:     3306
Database: payslip_db
Username: payslip_user
Password: payslip_pass123
```

> เพิ่ม `allowPublicKeyRetrieval=true&useSSL=false` ใน connection URL หากเชื่อมต่อไม่ได้

---

## Test Users

### Admin / HR

| Field | Value |
|-------|-------|
| Username | `admin` |
| Password | `admin1234` |
| URL | http://localhost:3000/admin/login |

### Employee

| Field | Value |
|-------|-------|
| National ID | `1101200132001` |
| Password | `1101200132001` (default = national ID) |
| URL | http://localhost:3000/employee/login |

> **หมายเหตุ:** รหัสผ่านเริ่มต้นของพนักงานคือเลขบัตรประชาชน ซึ่งจะถูกสร้างอัตโนมัติเมื่อ Admin upload Excel

---

## Features

### Admin / HR
- Login เข้าสู่ระบบ
- Upload ไฟล์ Excel ข้อมูลเงินเดือนพนักงาน
- ระบบ Validate ข้อมูลก่อนบันทึก — หากมี error แม้แต่ row เดียว จะไม่บันทึก
- Download Error File เป็น Excel พร้อม error message ในแต่ละ row
- ดูผลการ Upload (success/failed records)
- ดูประวัติการ Upload ทั้งหมด
- Download ไฟล์ต้นฉบับและ error file จากประวัติ
- ดูข้อมูลเงินเดือนพนักงานทั้งหมด filter ตามเดือน/ปี

### Employee
- Login ด้วยเลขบัตรประชาชน 13 หลัก
- ดูรายการสลิปเงินเดือนของตนเอง
- Filter ตามเดือน/ปี
- ดูรายละเอียดสลิปเงินเดือน
- Download สลิปเป็น PDF
- เห็นเฉพาะข้อมูลของตนเองเท่านั้น

---

## Excel Format

ไฟล์ Excel ที่ใช้ Upload ต้องมี column ดังนี้ (row แรกเป็น header):

| Column | Required | Description |
|--------|----------|-------------|
| No | - | ลำดับ |
| เลขรหัส / ID | ✅ | รหัสพนักงาน |
| ชื่อ-สกุล / Name | ✅ | ชื่อ-นามสกุล |
| ID Card | ✅ | เลขบัตรประชาชน 13 หลัก |
| แผนก / Department | ✅ | แผนก |
| ตำแหน่ง / Position | ✅ | ตำแหน่ง |
| วันเริ่มทำงาน / Start Working | - | วันที่เริ่มงาน |
| เงินเดือน / Salary | ✅ | เงินเดือน |
| Paid Salary | ✅ | เงินเดือนที่จ่าย |
| Allowance | - | เบี้ยเลี้ยง |
| จำนวนชั่วโมงทำงานล่วงเวลา / Total Overtime | - | OT |
| สวัสดิการรวมทั้งหมด / Total Allowance | - | สวัสดิการรวม |
| รายการปรับ / Adjust | - | รายการปรับ |
| Special | - | พิเศษ |
| รายรับทั้งหมด / Total Income | - | รายรับรวม |
| รายการหัก /Deduct | - | รายการหัก |
| ประกันสังคม | - | ประกันสังคม |
| TAX | - | ภาษี |
| กองทุนสำรองเลี้ยงชีพ | - | PVD |
| หักลดหย่อน | - | ลดหย่อน |
| กองทุนสงเคราะห์ลูกจ้าง | - | กองทุนสงเคราะห์ |
| รวมรายการหัก | - | รวมหัก |
| รวมทั้งหมด / Total Payment | ✅ | ยอดสุทธิ |
| รายได้สะสมประจำปี 2568 | - | YTD Income |
| ประกันสังคมสะสม ประจำปี 2568 | - | YTD SSO |
| Total TAX | - | YTD Tax |

ดูไฟล์ตัวอย่างได้ที่ `file_test_payslip.xlsx`

---

## Database Schema

### Tables

```
admins
├── id (PK)
├── username (UNIQUE)
├── password_hash
├── email
└── created_at

employees
├── id (PK)
├── national_id (UNIQUE) ← ใช้ login
├── employee_code (UNIQUE)
├── first_name, last_name
├── department, position
├── start_date
├── password_hash
└── created_at

upload_history
├── id (PK)
├── admin_id (FK → admins)
├── filename
├── original_file (BLOB)
├── error_file (BLOB)
├── month, year
├── total/success/failed_records
├── status (completed/failed)
└── uploaded_at

payslips
├── id (PK)
├── employee_id (FK → employees)
├── upload_id (FK → upload_history)
├── month, year
├── [earnings columns]
├── [deduction columns]
├── net_pay
├── [ytd columns]
└── created_at
```

### Relationships
- `admins` 1 → N `upload_history`
- `employees` 1 → N `payslips`
- `upload_history` 1 → N `payslips`

---

## Security

- Password hashed with bcrypt
- JWT Authentication (8 hours expiry)
- Role-based access control (Admin / Employee)
- Employee can only view their own data
- SQL Injection protection via SQLAlchemy ORM
- Duplicate upload prevention per month/year

---

## API Documentation

Swagger UI: http://localhost:8000/docs