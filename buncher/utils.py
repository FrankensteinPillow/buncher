from datetime import date


def get_date_from_string(date_str: str) -> date:
    return date.fromisoformat(date_str)
