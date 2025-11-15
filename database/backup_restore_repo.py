import os
import subprocess
from datetime import datetime
from pathlib import Path
from database.db_config import db_config


class BackupRepo:

    @staticmethod
    def create_backup(backup_dir: str) -> str:
        """
        Create a MySQL database backup (.sql file).
        Returns the backup file path.
        """
        Path(backup_dir).mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(backup_dir, f"backup_{timestamp}.sql")

        cmd = [
            "mysqldump",
            f"-h{db_config['host']}",
            f"-u{db_config['user']}",
            f"-p{db_config['password']}",
            db_config["database"]
        ]

        with open(backup_file, "w", encoding="utf-8") as f:
            result = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, text=True)

        if result.returncode != 0:
            raise RuntimeError(f"Backup failed: {result.stderr.strip()}")

        return backup_file

    @staticmethod
    def restore_backup(backup_file: str) -> None:
        """
        Restore a MySQL database from a backup file.
        """
        if not os.path.exists(backup_file):
            raise FileNotFoundError(f"Backup file not found: {backup_file}")

        cmd = [
            "mysql",
            f"-h{db_config['host']}",
            f"-u{db_config['user']}",
            f"-p{db_config['password']}",
            db_config["database"]
        ]

        with open(backup_file, "r", encoding="utf-8") as f:
            result = subprocess.run(cmd, stdin=f, stderr=subprocess.PIPE, text=True)

        if result.returncode != 0:
            raise RuntimeError(f"Restore failed: {result.stderr.strip()}")
