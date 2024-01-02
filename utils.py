import re
from datetime import datetime


def get_channel(content: str) -> int:
    pattern = r'<#(\d+)>'
    match = re.match(pattern, content)

    if match: 
        return int(content[2:-1])
    else: 
        return None
    

def get_datetime(datetime_str: str) -> str:
    datetime_str += ":00"
    try:
        datetime_object = datetime.strptime(datetime_str, '%d/%m/%y %H:%M:%S')
    except Exception:
        return None
    
    if datetime_object <= datetime.now():
        return None
    
    return datetime_str
