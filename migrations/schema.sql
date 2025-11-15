create database babu;
use babu;
CREATE TABLE accounts (
    acc_id INT AUTO_INCREMENT PRIMARY KEY,
    account_code CHAR(8) UNIQUE,   -- 8-digit structured code
    title VARCHAR(100) NOT NULL,
    account_type ENUM('SYSTEM', 'SUPPLIER', 'CUSTOMER') NOT NULL,
    unit VARCHAR(50) NULL,              -- e.g. 'Army', 'Civil', 'Cash', 'Revenue'
    cell VARCHAR(20) NULL,
    status ENUM('ACTIVE', 'INACTIVE') DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
 
INSERT INTO accounts (account_code, title, account_type, unit, cell, status)
VALUES 
('10000001', 'Cash Account', 'SYSTEM', 'Cash', '03001234567', 'ACTIVE'),
('10000002', 'Sales Revenue', 'SYSTEM', 'Sales', '03009876543', 'ACTIVE'),
('10000003', 'Purchase Expense', 'SYSTEM', 'Purchase', '03007654321', 'ACTIVE');

INSERT INTO accounts (account_code, title, account_type, unit, cell, status)
VALUES 
('20000001', 'ABC Suppliers', 'SUPPLIER', 'Civil', '03009876543', 'ACTIVE'),
('30002300', 'XYZ Customers', 'CUSTOMER', 'Army', '03007654321', 'ACTIVE');

DELIMITER $$

CREATE TRIGGER trg_generate_account_code
BEFORE INSERT ON accounts
FOR EACH ROW
BEGIN
    DECLARE prefix CHAR(2);
    DECLARE next_num INT;
    DECLARE base_num INT;

    -- Decide prefix and base number
    IF NEW.account_type = 'SYSTEM' THEN
        SET prefix = '10';
        SET base_num = 1;
    ELSEIF NEW.account_type = 'SUPPLIER' THEN
        SET prefix = '20';
        SET base_num = 1;
    ELSEIF NEW.account_type = 'CUSTOMER' THEN
        SET prefix = '30';
        SET base_num = 2300;   -- Start CUSTOMER accounts from 30002300
    END IF;

    -- Find the max existing code for this prefix
    SELECT IFNULL(MAX(CAST(SUBSTRING(account_code, 3, 6) AS UNSIGNED)), base_num - 1) + 1
    INTO next_num
    FROM accounts
    WHERE LEFT(account_code, 2) = prefix;

    -- Build the new code (prefix + 6-digit sequence, zero-padded)
    SET NEW.account_code = CONCAT(prefix, LPAD(next_num, 6, '0'));
END$$

DELIMITER ;


--     -- Trigger for auto-generating account codes
-- DELIMITER $$

-- CREATE TRIGGER trg_generate_account_code
-- BEFORE INSERT ON accounts
-- FOR EACH ROW
-- BEGIN
--     DECLARE prefix CHAR(2);
--     DECLARE next_num INT;

--     -- Decide prefix based on account_type
--     IF NEW.account_type = 'SYSTEM' THEN
--         SET prefix = '10';
--     ELSEIF NEW.account_type = 'SUPPLIER' THEN
--         SET prefix = '20';
--     ELSEIF NEW.account_type = 'CUSTOMER' THEN
--         SET prefix = '30';
--     END IF;

--     -- Find the max existing code for this prefix
--     SELECT IFNULL(MAX(CAST(SUBSTRING(account_code, 3, 6) AS UNSIGNED)), 0) + 1
--     INTO next_num
--     FROM accounts
--     WHERE LEFT(account_code, 2) = prefix;

--     -- Build the new code (prefix + 6-digit sequence, zero-padded)
--     SET NEW.account_code = CONCAT(prefix, LPAD(next_num, 6, '0'));
-- END$$

-- DELIMITER ;

select * from accounts;


CREATE TABLE IF NOT EXISTS ledger_entries (
    ledger_id INT AUTO_INCREMENT PRIMARY KEY,
    account_code CHAR(8) not null,
    date DATE NOT NULL,
    voucher_type ENUM('SALE', 'PURCHASE', 'CR', 'CP', 'JV','ADVANCE') NOT NULL,
    voucher_id INT NOT NULL,
    debit DECIMAL(12,2) DEFAULT 0.00,
    credit DECIMAL(12,2) DEFAULT 0.00,
    balance DECIMAL(12,2) DEFAULT 0.00,
    description VARCHAR(255),

    CONSTRAINT fk_ledger_account FOREIGN KEY (account_code)
        REFERENCES accounts(account_code)
        ON DELETE CASCADE
);


select * from ledger_entries;

CREATE TABLE IF NOT EXISTS products (
    product_id INT auto_increment primary KEY,
    company VARCHAR(100) NOT NULL,
    name VARCHAR(150) NOT NULL,
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

select * from products;

CREATE TABLE IF NOT EXISTS sales_invoice (
    invoice_no INT PRIMARY KEY AUTO_INCREMENT,
    date DATE NOT NULL,
    account_code CHAR(8) not null,
    advance DECIMAL(10,2) DEFAULT 0,
    total_amount DECIMAL(10,2) DEFAULT 0,
    remaining_balance DECIMAL(10,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
ALTER TABLE sales_invoice AUTO_INCREMENT = 2284;

select * from sales_invoice;

CREATE TABLE IF NOT EXISTS sales_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    invoice_no INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    purchase_rate DECIMAL(10,2) NOT NULL,
    retail_price DECIMAL(10,2) NOT NULL,
    amount DECIMAL(10,2) AS (quantity * retail_price) STORED,
    FOREIGN KEY (invoice_no) REFERENCES sales_invoice(invoice_no),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

select * from sales_items;

CREATE TABLE IF NOT EXISTS purchases (
    purchase_id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    account_code CHAR(8) not null,
    total_amount DECIMAL(12,2) NOT NULL,
    FOREIGN KEY (account_code) REFERENCES accounts(account_code) ON DELETE CASCADE
);

select * from purchases;
-- Table for Purchase Items (details)
CREATE TABLE IF NOT EXISTS purchase_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    purchase_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    purchase_rate DECIMAL(12,2) NOT NULL,
    amount DECIMAL(12,2) AS (quantity * purchase_rate) STORED,
    FOREIGN KEY (purchase_id) REFERENCES purchases(purchase_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

select * from purchase_items;

-- CR Voucher Header
CREATE TABLE cash_receivable_vouchers (
    voucher_id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
select * from cash_receivable_vouchers;
-- CR Voucher Entries (linked to voucher_id)
CREATE TABLE cash_receivable_entries (
    entry_id INT AUTO_INCREMENT PRIMARY KEY,
    voucher_id INT NOT NULL,
    account_code CHAR(8) not null,
    amount DECIMAL(12,2) NOT NULL,
    description VARCHAR(255) DEFAULT 'Payment received from customer',
    FOREIGN KEY (voucher_id) REFERENCES cash_receivable_vouchers(voucher_id),
    FOREIGN KEY (account_code) REFERENCES accounts(account_code)
);

select * from cash_receivable_entries;


-- CP Voucher Header
CREATE TABLE cash_payment_vouchers (
    voucher_id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
select * from cash_payment_vouchers;
-- CP Voucher Entries (linked to voucher_id)
CREATE TABLE cash_payment_entries (
    entry_id INT AUTO_INCREMENT PRIMARY KEY,
    voucher_id INT NOT NULL,
    account_code CHAR(8) not null,
    amount DECIMAL(12,2) NOT NULL,
    description VARCHAR(255) DEFAULT 'Payment made',
    FOREIGN KEY (voucher_id) REFERENCES cash_payment_vouchers(voucher_id),
    FOREIGN KEY (account_code) REFERENCES accounts(account_code)
);
select * from cash_payment_entries;

-- JV Voucher Header
CREATE TABLE journal_vouchers (
    voucher_id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    narration VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
select * from journal_vouchers;
-- JV Voucher Entries
CREATE TABLE journal_entries (
    entry_id INT AUTO_INCREMENT PRIMARY KEY,
    voucher_id INT NOT NULL,
    account_code CHAR(8) not null,
    debit DECIMAL(12,2) DEFAULT 0.00,
    credit DECIMAL(12,2) DEFAULT 0.00,
    description VARCHAR(255),
    FOREIGN KEY (voucher_id) REFERENCES journal_vouchers(voucher_id),
    FOREIGN KEY (account_code) REFERENCES accounts(account_code)
);
select * from journal_entries;

-- For finding latest CR per account quickly
CREATE INDEX idx_ledger_cr_date 
ON ledger_entries (voucher_type, account_code, date, ledger_id);

-- For balance calculation
CREATE INDEX idx_ledger_account 
ON ledger_entries (account_code, debit, credit);





-- Create separate cash_memo table
CREATE TABLE cash_memo (
    memo_no INTEGER PRIMARY KEY auto_increment,
    memo_date DATE NOT NULL,
    customer_name VARCHAR(255),
    contact_no VARCHAR(50),
    total_amount DECIMAL(15,2) NOT NULL,
    amount_paid DECIMAL(15,2) NOT NULL,
    change_amount DECIMAL(15,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
select * from cash_memo;
-- Create cash_memo_items table
CREATE TABLE cash_memo_items (
    id INTEGER PRIMARY KEY auto_increment,
    memo_no INTEGER NOT NULL,
    product_id int NOT NULL,
    quantity INTEGER NOT NULL,
    purchase_rate DECIMAL(15,2) NOT NULL,
    retail_rate DECIMAL(15,2) NOT NULL,
    amount DECIMAL(15,2) NOT NULL,
    FOREIGN KEY (memo_no) REFERENCES cash_memo(memo_no) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
select * FROM cash_memo_items;
-- Create index for better performance
CREATE INDEX idx_cash_memo_date ON cash_memo(memo_date);
CREATE INDEX idx_cash_memo_items_memo ON cash_memo_items(memo_no);









SELECT 
    cre.entry_id,
    cre.account_code,
    a.title,       -- adjust column name if different
    cre.amount AS entry_amount,
    
    -- totals from ledger (already aggregated in subquery)
    COALESCE(l.total_debit, 0) AS total_debit,
    COALESCE(l.total_credit, 0) AS total_recoveries,
    COALESCE(l.balance, 0) AS balance

FROM cash_receivable_entries cre
JOIN accounts a 
    ON cre.account_code = a.account_code
LEFT JOIN (
    SELECT 
        le.account_code,
        SUM(debit) AS total_debit,
        SUM(credit) AS total_credit,
        COALESCE(SUM(debit),0) - COALESCE(SUM(credit),0) AS balance
    FROM ledger_entries le
    GROUP BY le.account_code
) l
    ON cre.account_code = l.account_code

WHERE cre.voucher_id = 7;
