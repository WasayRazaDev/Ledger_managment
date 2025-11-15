# from pathlib import Path
# from datetime import datetime


# def log_update(voucher_type: str, voucher_id, details: str = "") -> None:
#     try:
#         project_root = Path(__file__).resolve().parent.parent
#         logs_dir = project_root / "logs"
#         logs_dir.mkdir(exist_ok=True)

#         log_file = logs_dir / "logs.txt"

#         # Migrate old root logs.txt to logs/logs.txt on first run
#         old_log = project_root / "logs.txt"
#         if old_log.exists() and not log_file.exists():
#             try:
#                 old_log.replace(log_file)
#             except Exception:
#                 pass

#         timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         line = f"{timestamp} | {voucher_type} | {voucher_id} | {details}\n"
#         with open(log_file, "a", encoding="utf-8") as f:
#             f.write(line)
#     except Exception:
#         pass


import sys
from pathlib import Path
from datetime import datetime

def log_update(voucher_type: str, voucher_id, details: str = "") -> None:
    try:
        if getattr(sys, 'frozen', False):
            # If exe is in dist/ledger_management_system/ or similar
            # base_dir = Path(sys.executable).parent
            # If you need to go up one level to reach project root:
            base_dir = Path(sys.executable).parent.parent
        else:
            base_dir = Path(__file__).resolve().parent.parent
        
        logs_dir = base_dir / "logs"
        logs_dir.mkdir(exist_ok=True)

        log_file = logs_dir / "logs.txt"

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"{timestamp} | {voucher_type} | {voucher_id} | {details}\n"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(line)
            
    except Exception:
        pass  # Silent fail as in your original code