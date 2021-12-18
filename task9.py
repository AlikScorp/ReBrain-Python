# Задание:
# Напишите скрипт, который:
#
# 1. Принимает в качестве параметров требуемое количество записей и задержку (соответственно, он должен запускаться
# с терминала с указанием необходимых параметров).
# 2. Выводит в файл log_file.log указанное количество строчек лога с указанной задержкой между записью строк.
# 3. Структура строки лога - Трехбуквенное обозначение текущего месяца, число месяца, время в формате ЧЧ:ММ:СС,
# уровень записываемого лога, сообщение. Разделитель между всеми элементами лога - пробел. Месяц от даты также должен
# отделять пробел.
# <месяц> <число> <часы>:<минуты>:<секунды> <уровень> <сообщение>
# 4. Содержание строки лога - сообщение с уровнем INFO, в котором вы передаете по одной переменной окружения в таком
# виде: <Имя переменной> -> <Содержание переменной>
# Пример записи лога:
#
# Jun 10 14:00:30 INFO NUMBER_OF_PROCESSORS -> 4
# Запустите скрипт и запишите 10 строк лога с задержкой 2 секунды между записями.

import logging
from sys import argv
from os import environ
from time import sleep


log = logging.getLogger('file_log')
log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%b %d %H:%M:%S')

file_log_handler = logging.FileHandler('log_file.log', 'w', 'utf-8')
file_log_handler.setFormatter(formatter)
file_log_handler.setLevel(logging.INFO)

log_handler = logging.StreamHandler()
log_handler.setFormatter(formatter)
log_handler.setLevel(logging.DEBUG)

log.addHandler(log_handler)
log.addHandler(file_log_handler)

if argv and len(argv) == 3:
    quantity = int(argv[1])
    delay = int(argv[2])
    step = 1
    log.debug(f'{quantity} environment variables will be processed with delay {delay} seconds.')
    for key, value in environ.items():
        if step <= quantity:
            step += 1
            log.info(f"{key} -> {value}")
            sleep(delay)
        else:
            break
else:
    log.debug("Cannot run without attributes.")
