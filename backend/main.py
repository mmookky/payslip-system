from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import admin, employee
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Self-Service Payslip API",
    description="API for Payroll system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin.router)
app.include_router(employee.router)


@app.get("/")
def root():
    return {"message": "Payslip API is running"}