# Напишите функции:
# нахождения корней квадратного уравнения
# генерации csv файла с тремя случайными числами в каждой строке 100-1000 строк.
# Декоратор, запускающий функцию нахождения корней квадратного уравнения с каждой тройкой чисел из csv файла.
# Декоратор, сохраняющий переданные параметры и результаты работы функции в json файл.

import csv
import json
from random import randint
from typing import Callable
import os
from time import time

def start_square(func: Callable):
    def wrapper(path_csv: str = 'numbers.csv'):
        nums_list = []
        res = {}
        result = {}
        with open(path_csv, 'r', encoding='UTF-8') as file:
            numbers = csv.reader(file, dialect='excel', quoting=csv.QUOTE_ALL)
            for line in numbers:
                if line:
                    nums_list.append(' '.join(line).split(' '))
            nums_list.pop(0)
            for i in range(len(nums_list)):
                res[i] = list(map(int, nums_list[i]))
            for key, value in res.items():
                result[key] = func(*value)
        # os.remove(path_csv)
        return result
    return wrapper


def json_save(func: Callable):
    def wrapper(path: str = 'square_results.json', *args, **kwargs):
        result = func(*args, **kwargs)
        if not os.path.exists(path):
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=4, ensure_ascii=False)
        else:
            with open(path, 'r', encoding='utf-8') as f_read:
                json_data = json.load(f_read)
            with open(path, 'a', encoding='utf-8') as f_write:
                json.dump(json_data, f_write, indent=4, ensure_ascii=False)
        return result
    return wrapper


@json_save
@start_square
def square(a: int, b: int, c: int):
    discriminant = b**2 - 4 * a * c
    if a and b:
        if discriminant > 0:
            x1 = (-b + discriminant ** 0.5) / 2 / a
            x2 = (-b - discriminant ** 0.5) / 2 / a
            return x1, x2
        elif discriminant == 0:
            x = -b / 2 / a
            return x
        else:
            return 'Вещественных корней нет'
    else:
        return 'На ноль делить нельзя'


def gen_csv(path_csv: str = 'numbers.csv', min_border: int = -100, max_border: int = 100):
    MIN_STR = 100
    MAX_STR = 1000
    with open(path_csv, 'w', encoding='UTF-8') as file:
        csv_writer = csv.writer(file, dialect='excel', delimiter=' ', quoting=csv.QUOTE_NONNUMERIC)
        csv_writer.writerow(('a', 'b', 'c'))
        dict_nums = {}
        for i in range(randint(MIN_STR, MAX_STR + 1)):
            while True:
                a = randint(min_border, max_border + 1)
                b = randint(min_border, max_border + 1)
                if a == 0 or b == 0:
                    continue
                else:
                    break
            c = randint(min_border, max_border + 1)
            dict_nums[i] = a, b, c
        csv_writer.writerows(dict_nums.values())


gen_csv()
square()
