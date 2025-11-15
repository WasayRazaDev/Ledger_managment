from database.backup_restore_repo import BackupRepo


class BackupService:

    @staticmethod
    def backup_database(backup_dir: str) -> str:
        return BackupRepo.create_backup(backup_dir)

    @staticmethod
    def restore_database(backup_file: str) -> None:
        BackupRepo.restore_backup(backup_file)
