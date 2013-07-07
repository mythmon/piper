from numbers import Number
from datetime import datetime


def coerce_datetime(input):
    if isinstance(input, datetime):
        return input

    if isinstance(input, basestring):
        try:
            input = float(input)
        except ValueError:
            # Not a float
            pass

    if isinstance(input, Number):
        # JS datetimes are milliseconds since the epoch. This guesses if
        # that is what we have here. As a result, seconds style dates
        # can't be after the year 20982, and millisecond style dates
        # can't be before 1990
        if input > 6e11:
            input /= 1000
        return datetime.fromtimestamp(input)

    print type(input)
    raise NotImplementedError
