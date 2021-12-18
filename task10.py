"""
    1. Напишите класс PC_memory, содержащий данные о памяти компьютера. Определите этому классу следующие методы:
    1.1. Конструктор __init__(), определяющий следующие атрибуты экземпляра класса при его создании (и принимающий
    значения для этих атрибутов в качестве аргументов):

        pc_id - id компьютера
        user_name - имя пользователя.
        memory_total - общий объем виртуальной памяти.
        memory_used - используемый объем виртуальной памяти.
        memory_percent - используемый процент виртуальной памяти. Этот атрибут может быть заполнен пользователем при
        создании экземпляра класса, или, в случае, если пользователь его не указал, рассчитываться автоматически исходя
        из атрибутов memory_total и memory_used

    1.2. Метод show_used_percent(), выводящий на экран процент занятой памяти по следующему шаблону:

        PC with id '<pc_id>' used <memory_percent> percent of memory

    1.3. Метод is_enough_memory() возвращающий False, если памяти осталось меньше 10% (процент свободной памяти меньше 10)
    или меньше 1Гб, а иначе возвращающий True.

    2. Создайте экземпляр класса и заполните его данными, полученными с помощью os.getlogin() и psutil.virtual_memory().
    Убедитесь, что у вас корректно работает расчет процента используемой памяти, если пользователь его не ввел.

    3. Примените к созданному экземпляру методы show_used_percent() и is_enough_memory(). Выведите результат работы метода
    is_enough_memory() на экран.
"""
from os import getlogin
from psutil import virtual_memory


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


name = getlogin()
v_memory = virtual_memory()

memory = PC_Memory(pc_id='My PC', user_name=name, memory_total=v_memory.total, memory_used=v_memory.used)
memory.show_used_percent()
print(f"Is memory enough: {memory.is_enough_memory()}")
