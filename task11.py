# Задание
# 1. Скопируйте ваш класс, который вы создали, выполняя задание предыдущего урока: PC_memory, содержащий данные о памяти
# компьютера. Напоминаем, что у этого класса определены следующие методы:
#
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
# 3. Создайте новый класс PC_advanced, наследуемый от PC_memory. Переопределите конструктор для нового класса, дополнив
# атрибуты, получаемые классом-родителем, следующими атрибутами:
# ld_avg_1m - количество процессов в очереди выполнения, усредненное за 1 минуту
# ld_avg_15m - количество процессов в очереди выполнения, усредненное за 15 минут
#
# Создайте для вашего нового класса 2 новых метода:
# 3.1. Метод is_overloaded() возвращает True, если количество процессов в очереди, усредненное за 1 минуту как минимум
# троекратно превышает количество процессов в очереди, усредненное за 15 минут. В остальных случаях возвращает False.
#
# 3.2. Метод __call__(), срабатывающий при вызове экземпляра как функции, должен принимать в качестве аргумента строку.
# Если строка 'memory' (по умолчанию), то возвращается результат работы метода is_enough_memory(), а если 'load', то
# возвращается результат работы метода is_overloaded(). В остальных случаях возвращается None.
#
# 4. Создайте экземпляр нового класса. Для заполнения атрибутов ld_avg_1m и ld_avg_15m вам поможет функция getloadavg()
# из библиотеки psutil.
#
# 5. Вызовите метод is_overloaded, и выведите результат его работы на экран
#
# 6. Вызовите экземпляр класса как функцию, не указывая ей никаких аргументов (аргумент должен браться по умолчанию).
# Выведите результат этого вызова на экран.

from os import getlogin
from psutil import virtual_memory, getloadavg


class PC_Memory:

    def __init__(self, pc_id: str, user_name: str, memory_total: int, memory_used: int, memory_percent: float = None):
        self.pc_id = pc_id
        self.user_name = user_name
        self.memory_total = memory_total
        self.memory_used = memory_used

        if memory_percent:
            self.memory_percent = memory_percent
        else:
            self.memory_percent = memory_used*100/memory_total

    def show_used_percent(self):
        print(f"PC with id '{self.pc_id}' used {self.memory_percent:2.2f} percent of memory")

    def is_enough_memory(self):
        if self.memory_percent < 10 or (self.memory_total - self.memory_used)/1024 ** 3 < 1:
            return False
        return True


class PC_Advance(PC_Memory):
    _ld_avg_1m: float
    _ld_avg_15m: float

    def __init__(self, pc_id: str, user_name: str, memory_total: int, memory_used: int,
                 ld_avg_1m: float, ld_avg_15m: float, memory_percent: float = None):

        super().__init__(pc_id, user_name, memory_total, memory_used, memory_percent)

        self._ld_avg_1m = ld_avg_1m
        self._ld_avg_15m = ld_avg_15m

    def is_overloaded(self):
        return self._ld_avg_1m/self._ld_avg_15m >= 3

    def __call__(self, string: str = 'memory', *args, **kwargs):
        if string == 'memory':
            return self.is_enough_memory()
        elif string == 'load':
            return self.is_overloaded()
        else:
            return


name = getlogin()
v_memory = virtual_memory()
loadavg = getloadavg()

memory = PC_Advance(pc_id='My PC', user_name=name, memory_total=v_memory.total, memory_used=v_memory.used,
                    ld_avg_1m=loadavg[0], ld_avg_15m=loadavg[2])

print(f"Is memory overloaded: {memory.is_overloaded()}")
print(f"Is enough memory: {memory()}")
