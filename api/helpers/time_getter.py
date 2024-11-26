from datetime import datetime
from zoneinfo import ZoneInfo

def parse_opening_time(opening_time: str | None, local_tz: str = "Europe/Moscow") -> datetime | None:
    if opening_time is None:
        return None
    
    # Преобразуем строку в datetime, сразу учитывая временную зону
    return datetime.strptime(opening_time, "%H:%M %d-%m-%Y") \
           .replace(tzinfo=ZoneInfo(local_tz)) \
           .astimezone(ZoneInfo("UTC")) \
           .replace(tzinfo=None)

