from datetime import datetime


def convert_datetime_to_iso_8601(dt: datetime, extended: bool = False) -> str:
    if extended:
        return dt.isoformat(timespec='milliseconds')
    return dt.strftime('%Y-%m-%dT%H:%M:%S')
