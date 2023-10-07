import random
from datetime import datetime, timedelta
from typing import Iterable


def get_random_value_occur_same_number(
    length_range: tuple[int, int] = (1, 15), numbers: Iterable[int] = (1, 2, 3, 4, 5, 6, 7, 8, 9)
) -> int:
    numbers = list(sorted(numbers))
    number = str(random.choice(numbers))
    return int(number * random.randint(length_range[0], length_range[1]))


def get_random_datetime_in_future(
    days_from=0,
    days_up_to=7,
    hours_from=0,
    hours_up_to=24,
    minutes_from=0,
    minutes_up_to=60,
    seconds_from=0,
    seconds_up_to=60,
) -> datetime:
    days = random.randint(days_from, days_up_to)
    hours = random.randint(hours_from, hours_up_to)
    minutes = random.randint(minutes_from, minutes_up_to)
    seconds = random.randint(seconds_from, seconds_up_to)
    return datetime.now() + timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)


def get_random_value_with_2_5_betavariate(from_, up_to) -> float:
    return 1 + random.betavariate(alpha=2, beta=5) * (from_ / up_to)
