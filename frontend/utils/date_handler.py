from datetime import datetime
from icecream import ic


from constants.constants import TailWindColors

ic.configureOutput(prefix="Debug | ", includeContext=True)


def ISO8601_to_std(date: str | datetime) -> str:
    if date is None:
        return None
    try:
        # If the input is already a datetime object, format it directly
        if isinstance(date, datetime):
            formatted_date = date.strftime("%d/%m/%y")
        # If it's a string in ISO8601 format, convert it first
        elif isinstance(date, str):
            datetime_obj = datetime.strptime(date[:19], "%Y-%m-%dT%H:%M:%S")
            formatted_date = datetime_obj.strftime("%d/%m/%y")
        else:
            return date  # Return as-is if the input type is unhandled
        return formatted_date
    except ValueError as e:
        print(f"Error: {e}")
        return date


def str_to_datetime(date: str):
    if date is None:
        return None
    try:
        return datetime.strptime(date, "%d/%m/%y")
    except ValueError as e:
        print(f"Error: {e}")
        return date


def color_due_date(created_date: datetime, due_date: datetime) -> tuple[str, str]:
    """
    Converts Due-Date Control's color According to Time Remaining for task to be completed.

    Args:
        created_date (datetime): datetime object to be passed when task is created.
        due_date (datetime): datetime object to be passed when task has due.

    Returns:
        tuple[str, str]: a color and message for flet control
    """
    days_passed = (due_date - created_date).days

    if days_passed <= 0:
        return TailWindColors.red_600, f"Days remaining: {days_passed}"
    if days_passed <= 7:
        return TailWindColors.orange_400, f"Days remaining: {days_passed}"
    if days_passed <= 20:
        return TailWindColors.yellow_300, f"Days remaining: {days_passed}"
    if days_passed <= 30:
        return TailWindColors.lime_300, f"Days remaining: {days_passed}"
    else:
        return TailWindColors.green_400, f"Days remaining: {days_passed}"


if __name__ == "__main__":
    print(ISO8601_to_std(datetime.now()))
    print(str_to_datetime("24/07/07").isoformat())
    print(color_due_date(datetime.now(), datetime(2024, 10, 31)))
