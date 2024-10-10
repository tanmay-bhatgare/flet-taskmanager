from datetime import datetime
from icecream import ic

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


if __name__ == "__main__":
    print(ISO8601_to_std(datetime.now()))
    print(str_to_datetime("24/07/07").isoformat())
