from datetime import datetime


def is_fizz_buzz(user):
    result = user.number
    if user.number % 3 == 0 and user.number % 5 == 0:
        result = "BizzFuzz"
    elif user.number % 5 == 0:
        result = "Fuzz"
    elif user.number % 3 == 0:
        result = "Bizz"
    return result


def get_age(user):
    return "allowed" if int(((datetime.today().date() - user.birthDate)/365.25).days) > 13 else "blocked"
