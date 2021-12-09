# Задание
# 1. Скопируйте к себе этот модифицированный список из 4го урока, отображающий количество общей и занятой памяти на
# накопителях (он был у вас и на предыдущем задании):
# [
#     {'id': 382, 'total': 999641890816, 'used': 228013805568},
#     {'id': 385, 'total': 61686008768, 'used': 52522710872},
#     {'id': 398, 'total': 149023482194, 'used': 83612310700},
#     {'id': 400, 'total': 498830397039, 'used': 459995976927},
#     {'id': 401, 'total': 93386008768, 'used': 65371350065},
#     {'id': 402, 'total': 988242468378, 'used': 892424683789},
#     {'id': 430, 'total': 49705846287, 'used': 9522710872},
# ]
# 2. Напишите функцию, которая:
# 2.1. Получает этот список
#
# 2.2. Анализирует состояние памяти каждого накопителя по алгоритму из задания для 4го урока. Напоминаю:
#
# Если свободной памяти осталось меньше 10Гб или меньше 5%, то на накопителе критически мало свободного места;
# Если свободной памяти больше, чем в предыдущем пункте, но меньше 30Гб или меньше 10%, то на накопителе мало
# свободного места;
# Иначе на накопителе достаточно свободного места
# 2.3. Функция должна представлять собой генератор (совершать вывод инструкцией yield), который воспроизводит одну
# итерацию для каждого словаря в получаемом списке
#
# 2.4. Результат работы функции на каждой итерации - словарь вида {'id': <id устройства>,
# 'memory_status': <статус памяти>}.
#
# Статусы могут быть такие: 'memory_ok', 'memory_not_enough' и 'memory_critical'.
#
# 3. Используя вашу функцию сформируйте список словарей статусов накопителей и объедините эти словари со словарями
# из основного списка (в результате к словарям в основном списке должно добавиться еще одно поле 'memory_status').
# Попробуйте сделать этот пункт в одно выражение (воспользуйтесь списковым включением).
#
# 4. Выведите итоговый список словарей на экран
#
# 5. Вам дан список логов:
#
# May 18 11:59:18 PC-00102 plasmashell[1312]: kf.plasma.core: findInCache with a lastModified timestamp of 0 is deprecated
# May 18 13:06:54 ideapad kwin_x11[1273]: Qt Quick Layouts: Detected recursive rearrange. Aborting after two iterations.
# May 20 09:16:28 PC0078 systemd[1]: Starting PackageKit Daemon...
# May 20 11:01:12 PC-00102 PackageKit: daemon start
# May 20 12:48:18 PC0078 systemd[1]: Starting Message of the Day...
# May 21 14:33:55 PC0078 kernel: [221558.992188] usb 1-4: New USB device found, idVendor=1395, idProduct=0025, bcdDevice= 1.00
# May 22 11:48:30 ideapad mtp-probe: checking bus 1, device 3: "/sys/devices/pci0000:00/0000:00:08.1/0000:03:00.3/usb1/1-4"
# May 22 11:50:09 ideapad mtp-probe: bus: 1, device: 3 was not an MTP device
# May 23 08:06:14 PC-00233 kernel: [221559.381614] usbcore: registered new interface driver snd-usb-audio
# May 24 16:19:52 PC-00233 systemd[1116]: Reached target Sound Card.
# May 24 19:26:40 PC-00102 rtkit-daemon[1131]: Supervising 5 threads of 2 processes of 1 users.
#
# 6. Используя лямбда-функцию отсортируйте этот список по времени (не по дате/времени) и выведите 3й элемент
# отсортированного списка.
#
# 7. Используя функцию filter() или списковые включения, сформируйте новый список, в который входят только логи,
# которые записал PC-00102.
#
# 8. Используя списковые включения, сформируйте список сообщений логов, которые записал процесс kernel.
# Необходимо составить список только из сообщений. Дату, время, имя ПК и имя сервиса включать не нужно.


def storage_analyzer(storages_list: list) -> dict:
    """
        Функция-генератор, анализирует состояние памяти каждого накопителя из storages_list
    :param storages_list:
    :return: Словарь вида {'id': <id устройства>, 'memory_status': <статус памяти>}
    """

    for list_item in storages_list:
        free_space: int = list_item['total'] - list_item['used']
        free_space_percent: float = free_space*100/list_item['total']
        free_space_in_gb: float = free_space / 1024 ** 3

        if free_space_percent <= 5 or free_space_in_gb <= 10:
            status = 'memory_critical'
        elif free_space_percent <= 10 or free_space_in_gb <= 30:
            status = 'memory_not_enough'
        else:
            status = 'memory_ok'

        yield {"id": list_item['id'], "memory_status": status}


storages: list = [
    {'id': 382, 'total': 999641890816, 'used': 228013805568},
    {'id': 385, 'total': 61686008768, 'used': 52522710872},
    {'id': 398, 'total': 149023482194, 'used': 83612310700},
    {'id': 400, 'total': 498830397039, 'used': 459995976927},
    {'id': 401, 'total': 93386008768, 'used': 65371350065},
    {'id': 402, 'total': 988242468378, 'used': 892424683789},
    {'id': 430, 'total': 49705846287, 'used': 9522710872},
]

log: list = [
    "May 18 11:59:18 PC-00102 plasmashell[1312]: kf.plasma.core: findInCache with a lastModified timestamp of 0 is deprecated",
    "May 18 13:06:54 ideapad kwin_x11[1273]: Qt Quick Layouts: Detected recursive rearrange. Aborting after two iterations.",
    "May 20 09:16:28 PC0078 systemd[1]: Starting PackageKit Daemon...",
    "May 20 11:01:12 PC-00102 PackageKit: daemon start",
    "May 20 12:48:18 PC0078 systemd[1]: Starting Message of the Day...",
    "May 21 14:33:55 PC0078 kernel: [221558.992188] usb 1-4: New USB device found, idVendor=1395, idProduct=0025, bcdDevice= 1.00",
    'May 22 11:48:30 ideapad mtp-probe: checking bus 1, '
    'device 3: "/sys/devices/pci0000:00/0000:00:08.1/0000:03:00.3/usb1/1-4"',
    'May 22 11:50:09 ideapad mtp-probe: bus: 1, device: 3 was not an MTP device',
    'May 23 08:06:14 PC-00233 kernel: [221559.381614] usbcore: registered new interface driver snd-usb-audio',
    'May 24 16:19:52 PC-00233 systemd[1116]: Reached target Sound Card.',
    'May 24 19:26:40 PC-00102 rtkit-daemon[1131]: Supervising 5 threads of 2 processes of 1 users.',
]

# Задание 3. Формируем список словарей статусов накопителей и объединяем словари
[a.update(b) for a, b in zip(storages, storage_analyzer(storages))]

print("\nЗадание №4. Выводим итоговый список словарей на экран")
for storage in storages:
    print(storage)

print('\nЗадание №6. Выводим 3й элемент отсортированного по времени списка.')
sorted_log: list = sorted(log, key=lambda a: a[7:15])
print(sorted_log[2])

print('\nЗадание №7. Список, в который входят только логи, которые записал PC-00102.')
pc_00102_list: list = [a for a in log if a.split(" ", 4)[3] == 'PC-00102']
for item in pc_00102_list:
    print(item)

print('\nЗадание №8. Список сообщений логов, которые записал процесс kernel.')
kernel_messages: list = [a[1] for a in map(lambda a: a.split(': ', 1), log) if a[0].split(" ")[-1] == "kernel"]

for message in kernel_messages:
    print(message)
