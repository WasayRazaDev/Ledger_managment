# Ledger Management System

A lightweight desktop ledger/accounting application built with Python and PyQt5. It provides basic bookkeeping features (sales, purchases, cash receipts/payments, journals, ledger statements) backed by a MySQL database.

## Features
- Double-entry ledger entries recorded in `ledger_entries` via repository layer
- GUI built with PyQt5 in the `ui/` package
- Services for posting, reversing and updating transactions (`core/transaction_service.py`)
- CRUD-style repositories in `database/` to interact with MySQL
- Backup/restore helpers and SQL migration assets in `backup/` and `migrations/`

## Requirements
- Python 3.8+ (project includes a virtual environment at `ledger_env/`)
- MySQL server
- Packages in `requirements.txt` (install with pip)

## Quick setup

1. (Recommended) Create and activate a virtual environment, or use the included `ledger_env`.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # PowerShell
pip install -r requirements.txt
```

2. Configure database connection in [database/db_config.py](database/db_config.py#L1).
	- IMPORTANT: Do not commit real credentials. Replace the values in that file or use environment variables.

3. Prepare the database schema. Example SQL files and seeds are in `migrations/`.

4. Run the application:

```powershell
python main.py
```

## Project layout (key files)
- `main.py` — application entry (creates PyQt5 `MainWindow`)
- `ui/` — PyQt5 UI modules and dialogs (main window, ledger views, vouchers)
- `core/` — domain services and models (ledger, transaction posting)
- `database/` — repository layer and `db_config.py` connection pool
- `backup/`, `migrations/` — backup SQL and migration scripts
- `ledger_env/` — included virtual environment (optional)

## Notes & security
- The repository currently includes a simple MySQL connection pool in [database/db_config.py](database/db_config.py#L1-L20). Update it to use secured credentials or environment variable injection before production use.
- The `requirements.txt` in this repo may be encoded in UTF-16; use `pip install -r requirements.txt` after ensuring proper encoding.

## Development tips
- Use `database/ledger_repo.py` and other `*_repo.py` modules as examples when adding new persistence logic.
- Transactions are posted with `core/transaction_service.py` which inserts corresponding debit and credit entries.

## Contributing
Pull requests and issues are welcome. Open an issue for feature requests or bugs.

---
If you'd like, I can also:
- run a quick static scan of code to produce a more detailed README (data model, tables),
- or update `database/db_config.py` to load credentials from environment variables.

