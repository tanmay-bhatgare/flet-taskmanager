from datetime import datetime
from icecream import ic

ic.configureOutput(prefix="Debug | ", includeContext=True)


def ISO8601_to_std(date: str) -> str:
    if date is None:
        return None
    try:
        datetime_obj = datetime.strptime(date[:19], "%Y-%m-%dT%H:%M:%S")
        formated_date = datetime_obj.strftime("%d/%m/%y")
        return formated_date
    except ValueError as e:
        ic(e)

        return date


if __name__ == "__main__":
    print(ISO8601_to_std("2024-10-03T10:22:17.212Z"))
