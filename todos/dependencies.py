from datetime import date, datetime


def get_current_time() -> date:
    return datetime.utcnow()
