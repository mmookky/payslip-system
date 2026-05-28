CREATE TABLE IF NOT EXISTS admins (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    username      VARCHAR(50)  NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    email         VARCHAR(100),
    created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS employees (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    national_id   CHAR(13)     NOT NULL UNIQUE,
    employee_code VARCHAR(20)  NOT NULL UNIQUE,
    first_name    VARCHAR(100) NOT NULL,
    last_name     VARCHAR(100) NOT NULL,
    department    VARCHAR(100),
    position      VARCHAR(100),
    start_date    DATE,
    password_hash VARCHAR(255) NOT NULL,
    created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS upload_history (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    admin_id        INT          NOT NULL,
    filename        VARCHAR(255) NOT NULL,
    original_file   LONGBLOB     NULL,
    error_file      LONGBLOB     NULL,
    month           INT          NOT NULL,
    year            INT          NOT NULL,
    total_records   INT  DEFAULT 0,
    success_records INT  DEFAULT 0,
    failed_records  INT  DEFAULT 0,
    status          VARCHAR(20)  DEFAULT 'completed',
    uploaded_at     DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_id) REFERENCES admins(id),
    UNIQUE KEY unique_upload (month, year)
);

CREATE TABLE IF NOT EXISTS payslips (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    employee_id      INT            NOT NULL,
    upload_id        INT            NOT NULL,
    month            INT            NOT NULL,
    year             INT            NOT NULL,

    base_salary      DECIMAL(12,2)  DEFAULT 0,
    paid_salary      DECIMAL(12,2)  DEFAULT 0,
    allowance        DECIMAL(12,2)  DEFAULT 0,
    overtime_hours   DECIMAL(8,2)   DEFAULT 0,
    total_allowance  DECIMAL(12,2)  DEFAULT 0,
    adjust           DECIMAL(12,2)  DEFAULT 0,
    special          DECIMAL(12,2)  DEFAULT 0,
    total_income     DECIMAL(12,2)  DEFAULT 0,

    deduct           DECIMAL(12,2)  DEFAULT 0,
    social_security  DECIMAL(12,2)  DEFAULT 0,
    tax              DECIMAL(12,2)  DEFAULT 0,
    provident_fund   DECIMAL(12,2)  DEFAULT 0,
    total_deductions DECIMAL(12,2)  DEFAULT 0,
    tax_allowance    DECIMAL(12,2)  DEFAULT 0,
    welfare_fund     DECIMAL(12,2)  DEFAULT 0,

    net_pay          DECIMAL(12,2)  DEFAULT 0,

    ytd_income       DECIMAL(12,2)  DEFAULT 0,
    ytd_tax          DECIMAL(12,2)  DEFAULT 0,
    ytd_sso          DECIMAL(12,2)  DEFAULT 0,

    created_at       DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (employee_id) REFERENCES employees(id),
    FOREIGN KEY (upload_id)   REFERENCES upload_history(id),
    UNIQUE KEY unique_payslip (employee_id, month, year)
);

-- Admin ex (password: admin1234)
INSERT INTO admins (username, password_hash, email) VALUES
('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iK9i', 'admin@company.com');

-- Employee ex (password: emp1234)
INSERT INTO employees (national_id, employee_code, first_name, last_name, department, position, start_date, password_hash) VALUES
('1101200132001', 'EMP001', 'AKT', 'Thailand', 'IT', 'Manager', '2025-01-01',
'$2b$12$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi');