import random


def get_random_value_occur_same_number(length_range=(1, 15), numbers=(1, 2, 3, 4, 5, 6, 7, 8, 9)) -> int:
    numbers = list(sorted(numbers))
    number = str(random.randint(numbers[0], numbers[-1]))
    return int(number * random.randint(length_range[0], length_range[1]))
