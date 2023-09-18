# 📌Объедините функции из прошлых задач.
# 📌Функцию угадайку задекорируйте:
# ○ декораторами для сохранения параметров,
# ○ декоратором контроля значений и
# ○ декоратором для многократного запуска.
# 📌Выберите верный порядок декораторов.

# Доработайте прошлую задачу добавив декоратор wraps в
# каждый из декораторов.


import json
import os
import random
from typing import Callable
from functools import wraps
from time import time


def json_safe(func: Callable):
    """Записывает json с указанием времени в качестве ключа"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if not os.path.exists(f'result.json'):
            print(result)
            with open(f'result.json', 'w', encoding='utf-8') as f:
                json.dump({time(): result}, f, indent=4, ensure_ascii=False)

        else:
            with open(f'result.json', 'r', encoding='utf-8') as f_read:
                json_data = json.load(f_read)
                print(json_data)
            with open(f'result.json', 'w', encoding='utf-8') as f_write:
                json_data[time()] = result
                json.dump(json_data, f_write, indent=4, ensure_ascii=False)

        return result

    return wrapper


def decor(loop: int):
    """Функция будет работать столько раз, сколько передадим в параметре"""
    def inner(func):
        result = []
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(loop):
                result.append(func(*args, **kwargs))
            return result

        return wrapper

    return inner


def check_nums(func: Callable):
    """Проверка диапазона чисел"""
    @wraps(func)
    def wrapper(l_lim: int, h_lim: int, tries_: int):
        if l_lim > h_lim or l_lim < 0 or h_lim > 100:
            l_lim = 1
            h_lim = 100
        if tries_ not in range(1, 11):
            tries_ = random.randint(1, 10)

        result = func(l_lim, h_lim, tries_)
        return result

    return wrapper


@decor(3)
@json_safe
@check_nums
def guess_number(low: int = 10, high: int = 100, tries: int = 10) -> str:
    """Игра угадайка"""
    count = 1
    number = random.randint(low, high)
    while count <= tries:
        my_num = int(input(f'{count} из {tries} попытка. Введите число от {low} до {high}: '))
        if my_num > number:
            print('Я загадал меньше')
        elif my_num < number:
            print('Я загадал больше')
        else:
            result = f'Да ты победил c {count} попытки, я загадал {number}'
            break
        count += 1
    else:
        result = f'Извини, но ты проиграл, все попытки закончились. Я загадал {number}'
    print(result)
    return result


# guess_number(-1, 1000, 15)
print(guess_number.__name__)
print(help(guess_number))
print(check_nums.__name__)
print(help(check_nums))
print(decor.__name__)
print(help(decor))
print(json_safe.__name__)
print(help(json_safe))