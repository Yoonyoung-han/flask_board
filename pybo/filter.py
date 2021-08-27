def format_datetime(value, fmt='%Y년 %m월 %d일 %H:%M'):
    if type(value) == str:
        return value.format(fmt)
    return value.strftime(fmt)