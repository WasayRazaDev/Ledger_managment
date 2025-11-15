class Account:
    def __init__(self, acc_id=None, account_code="", title="", cell="", account_type=None, unit=None, status="active", created_at=None):
        self.acc_id = acc_id
        self.account_code = account_code
        self.title = title
        self.cell = cell
        self.account_type = account_type
        self.unit = unit
        self.status = status
        self.created_at = None

    def __repr__(self):
        return f"<Account {self.acc_id} - {self.title} ({self.status})>"
