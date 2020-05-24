import sys


def get_year(date):
    year = int(date[0])
    if 2000 <= year <= 2999:
        return year
    if year <= 999:
        return year + 2000
    return 0


def is_leap_year(year):
    return (year % 100 != 0 and year % 4 == 0) or year % 400 == 0


def is_date_valid(year, month, day):
    valid = False
    months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    if 1 <= month <= 12:
        if 1 <= day <= months[month - 1]:
            valid = True
        elif day == months[month - 1] + 1 and is_leap_year(year):
            valid = True

    return valid


def print_date(date_string):
    input_date = date_string.split("/")
    year = get_year(input_date)
    month = int(input_date[1])
    day = int(input_date[2])

    if is_date_valid(year, month, day):
        """zero padding for months and days as required"""
        input_date[0] = str(year)
        input_date[1] = "0" + str(month) if 0 < month < 10 else str(month)
        input_date[2] = "0" + str(day) if 0 < day < 10 else str(day)
        return "-".join(input_date)
    else:
        return date_string + " is illegal"


src = sys.argv[1]
with open(src, "r") as file:
    print(print_date(file.read().strip()))

