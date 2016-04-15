import calendar
import datetime


def get_month_day_range(date):
    """
    For a date 'datetime' returns the start and end date for the month of 'date'.
    """
    date = date.date() if isinstance(date, datetime.datetime) else date

    first_day = date.replace(day=1)
    last_day = date.replace(day=calendar.monthrange(date.year, date.month)[1])
    return first_day, last_day
