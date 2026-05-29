import asyncio
import os

import aiomysql
import bcrypt
from dotenv import load_dotenv

load_dotenv()


async def wait_for_db():
    for i in range(30):
        try:
            conn = await aiomysql.connect(
                host=os.getenv("DB_HOST", "db"),
                port=int(os.getenv("DB_PORT", 3306)),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                db=os.getenv("DB_NAME"),
            )
            print("✓ Connected to DB")
            return conn
        except Exception as e:
            print(f"Waiting for DB... ({i + 1}/30): {e}")
            await asyncio.sleep(2)
    raise RuntimeError("Could not connect to DB after 30 retries")


async def seed():
    conn = await wait_for_db()

    async with conn.cursor() as cur:
        admin_hash = bcrypt.hashpw(
            os.getenv("ADMIN_PASSWORD", "admin1234").encode("utf-8"), bcrypt.gensalt(12)
        ).decode("utf-8")

        emp_national_id = "1101200132001"
        emp_hash = bcrypt.hashpw(
            os.getenv("EMP_PASSWORD", emp_national_id).encode("utf-8"),
            bcrypt.gensalt(12),
        ).decode("utf-8")

        await cur.execute(
            "INSERT IGNORE INTO admins (username, password_hash, email) VALUES (%s, %s, %s)",
            ("admin", admin_hash, "admin@company.com"),
        )
        await cur.execute(
            """INSERT IGNORE INTO employees
               (national_id, employee_code, first_name, last_name, department, position, start_date, password_hash)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (
                emp_national_id,
                "EMP001",
                "AKT",
                "Thailand",
                "IT",
                "Manager",
                "2025-01-01",
                emp_hash,
            ),
        )

        await conn.commit()
        print("✓ Admin and employee seeded")

    conn.close()


if __name__ == "__main__":
    asyncio.run(seed())
