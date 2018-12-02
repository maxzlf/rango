import datetime


def delta_seconds(input_time):
    assert isinstance(input_time, datetime.datetime)
    input_time = input_time.replace(tzinfo=None)
    now = datetime.datetime.now()
    return abs((now - input_time).total_seconds())
