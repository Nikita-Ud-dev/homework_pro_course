# 1. Рядки (Strings):

#   a. Напишіть функцію, яка приймає рядок і повертає його довжину.
def length(string: str):
    if not string:
        return 0
    with_spaces = len(string)
    no_spaces = len("".join(string.split()))
    return f"Довжина рядка з пробілами: {with_spaces}, і без пробілів: {no_spaces}"
print(length("  string1"))
print(length("string1"))

#   b. Створіть функцію, яка приймає два рядки і повертає об'єднаний рядок.
def association_str(string1: str, string2: str) -> str:
    if not string1 or not string2:
        return ""
    return string1 + string2
print(association_str(string1="string) ", string2=" (string"))

# 2. Числа (Int/float):

#   c. Реалізуйте функцію, яка приймає число і повертає його квадрат.
def sq(num:int) -> int:
    return num ** 2
print(sq(5))

#   d. Створіть функцію, яка приймає два числа і повертає їхню суму.
def sum_numb(num1: int, num2: int) -> int:
    return num1 + num2
print(sum_numb(num1=2, num2=3))

#   e. Створіть функцію яка приймає 2 числа типу int, виконує операцію ділення та повертає чілу частину і залишок.
def divide(num1: int, num2: int):
    return divmod(num1, num2)
print(divide(125, 35))

# 3. Списки (Lists):

#   f. Напишіть функцію для обчислення середнього значення списку чисел.
def average_numb(lst: list[int | float]) -> float:
    if not lst:
        return 0.0
    return sum(lst) / len(lst)

#   g. Реалізуйте функцію, яка приймає два списки і повертає список, який містить спільні елементи обох списків.
def shared_facilities(lst1: list, lst2: list) -> list:
    if not lst1 or not lst2:
        return []
    st1, st2 = set(lst1), set(lst2)
    result = []
    result.extend(list(st1.intersection(st2)))
    return result
print(shared_facilities(lst1=[1,2,3,4,8,23,785,13566787,35,34], lst2=[3,512,23221,5,12344,8,134676,35]))
print(shared_facilities([],[12]))

# 4. Словники (Dictionaries):

#   h. Створіть функцію, яка приймає словник і виводить всі ключі цього словника.
def dictionary_keys(dct: dict):
    if not dct:
        return []
    return list(dct.keys())
print(dictionary_keys({12:None, 13:None, 14:None}))

#   i. Реалізуйте функцію, яка приймає два словники і повертає новий словник, який є об'єднанням обох словників.
def association_dict(dct1: dict, dct2: dict) -> dict:
    for key, value in dct2.items():
        dct1[key] = value
    return dct1
print(association_dict({"name": "Alexander", "lastname": "Tsin"}, {"age": 36, "group": "PN121"}))

# 5. Множини (Sets):

#   j. Напишіть функцію, яка приймає дві множини і повертає їхнє об'єднання.
def association_set(st1: set, st2: set) -> set:
    return st1.union(st2)
print(association_set({1,2,3,4,5}, {1,2,3,4,5,6,7,8,9,0}))

#   k. Створіть функцію, яка перевіряє, чи є одна множина підмножиною іншої.
def a_subset(st1: set, st2: set) -> bool:
    if not st1 or not st2:
        return True
    if len(st1.intersection(st2)) == len(st1):
        return True
    return False
print(a_subset(st1 = {1, 2}, st2 = {1, 2, 3}))
print(a_subset(st1 = {1, 4}, st2 = {1, 2, 3}))

# 6. Умовні вирази та цикли:

#  l. Реалізуйте функцію, яка приймає число і виводить "Парне", якщо число парне, і "Непарне", якщо непарне.
def even_or_no(num: int) -> str:
    if num % 2 == 0:
        return f"Парне число: {num}"
    return f"Непарне число: {num}"
print(even_or_no(14))

#   m. Створіть функцію, яка приймає список чисел і повертає новий список, що містить тільки парні числа.
def even_list(lst: list) -> list:
    even_lst = []
    for num in lst:
        if num % 2 == 0:
            even_lst.append(num)

    return even_lst