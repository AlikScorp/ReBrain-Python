# Задание
# 1. Скопируйте ваш класс, который вы создали, выполняя задание 11 урока: PC_memory, содержащий данные о памяти
# компьютера. Напоминаем, что у этого класса определены следующие методы:
# 1.1. Конструктор __init__(), определяющий следующие атрибуты экземпляра класса при его создании:
# pc_id - id компьютера
# user_name - имя пользователя.
# memory_total - общий объем виртуальной памяти.
# memory_used - используемый объем виртуальной памяти.
# memory_percent - используемый процент виртуальной памяти. Этот атрибут может быть заполнен пользователем при создании
# экземпляра класса, или, в случае, если пользователь его не указал, рассчитываться автоматически исходя из атрибутов
# memory_total и memory_used
#
# 1.2. Метод show_used_percent(), выводящий на экран процент занятой памяти по следующему шаблону:
# PC with id '<pc_id>' used <memory_percent> percent of memory
#
# 1.3. Метод is_enough_memory() возвращающий False, если памяти осталось меньше 10% или меньше 1Гб, а иначе
# возвращающий True
#
# 2. Дополните этот класс:
# 2.1. Преобразовывайте введенное пользователем значение используемой и общей памяти в целое число.
#
# 2.2. Самостоятельно возбуждайте ValueError в случаях, если значения используемой или общей памяти меньше 0, или если
# используемая память превышает общую.
#
# 2.3. Отлавливайте ValueError, возникающие по вышеуказанным причинам (по пункту 2.1 и по пункту 2.2). В случае
# возникновения таких исключений, вы должны:
#  - выводить на монитор следующую фразу: wrong memory value, default value used
#  - записывать в атрибуты класса значения по умолчанию: в общую память 100Гб, в используемую память и процент - 0.
#
# 2.4. Преобразовывайте процент используемой памяти, введенный пользователем, во float. Если это не удается
# (ValueError), то обрабатывайте это исключение следующим образом:
# - выводите на экран фразу: wrong percent value, value calculated automatically
# - записывайте в атрибут класса memory_percent значение, посчитанное автоматически исходя из значений memory_total и
# memory_used.
#
# 3. Создайте свое исключение PercentError.
# 3.1. Наследуйте его от Exception и ничего в нем не меняйте (оставьте ему тело pass). Вызывайте срабатывание этого
# исключения в случае, если пользователь ввел процент занятой памяти меньше 0 или больше 100.
#
# 3.2. Передавайте этому исключению строку 'Percent value must be between 0 and 100' в качестве аргумента.
# Не перехватывайте это исключение, пусть вызывает ошибку.
#
# 4. Попробуйте ввести некорректные данные:
# - нечисловую строку
# - слишком большое количество используемой памяти
# - отрицательное значение памяти
# Посмотрите, как себя ведет ваша программа в этом случае. Попробуйте ввести некорректный процент занятой памяти.
# Посмотрите, как срабатывает ваше созданное исключение и какие данные оно передает.

from os import getlogin
from psutil import virtual_memory


class PercentError(Exception):
    pass


class PC_Memory:

    def __init__(self, pc_id: str, user_name: str, memory_total: int, memory_used: int, memory_percent: float = None):
        self.pc_id = pc_id
        self.user_name = user_name

        try:
            self.memory_total = int(memory_total)
            self.memory_used = int(memory_used)

            if self.memory_total < 0 or self.memory_used < 0 or self.memory_used > self.memory_total:
                raise ValueError
        except ValueError:
            print("Wrong memory value, default value used")
            self.memory_total = 100*1024**3
            self.memory_used = 0
            self.memory_percent = 0

        try:
            self.memory_percent = float(memory_percent)
            if self.memory_percent < 0 or self.memory_percent > 100:
                raise PercentError('Percent value must be between 0 and 100')
        except (ValueError, TypeError):
            print("Wrong percent value, value calculated automatically")
            self.memory_percent = self.memory_used*100/self.memory_total

    def show_used_percent(self):
        print(f"PC with id '{self.pc_id}' used {self.memory_percent:2.2f} percent of memory")

    def is_enough_memory(self):
        if self.memory_percent < 10 or (self.memory_total - self.memory_used)/1024 ** 3 < 1:
            return False
        return True


name = getlogin()
v_memory = virtual_memory()

print('\nTesting memory_total is string:')
string_except_integer = PC_Memory(user_name=name, pc_id='My PC', memory_total='string', memory_used=100)
print("\nTesting memory_total is less than memory_used:")
used_more_than_total = PC_Memory(user_name=name, pc_id='My PC', memory_total=50, memory_used=100)
print("\nTesting memory_total has negative value:")
negative_memory_value = PC_Memory(user_name=name, pc_id='My PC', memory_total=-256, memory_used=100)
print("\nTesting memory_percent is not correct:")
incorrect_memory_percent = PC_Memory(user_name=name, pc_id='My PC', memory_total=256*1024**3, memory_used=32*1024**3,
                                     memory_percent=101)
