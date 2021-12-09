# Задание:
# 1. Вы получили такую строку логов:
#
# 'May 24 12:48:31 ideapad systemd[1]: logrotate.service: Succeeded.'
# Совершите над ней следующие действия:
#
# 1.1. Выделите и выведите на экран дату и время.
# 1.2. Выделите и выведите на экран название сервиса (systemd[1]), записавшего лог.
# 1.3. Замените название ПК (ideapad) на PC-12092, выведите полученную строку на экран.
# 1.4. Найдите в логе слово failed и выведите его позицию, если такого слова нет, выведите -1.
# 1.5. Посчитайте количество букв 'S' в строке вне зависимости от регистра (и прописных, и заглавных).
# 1.6. Выделите из строки значения часов, минут и секунд, суммируйте эти 3 числа и выведите полученное число на экран.
#
# Вы получили такую строку логов:
# 'May 24 14:03:01 ideapad colord[844]: failed to get session [pid 8279]: Нет доступных данных'
# Нужно сформировать и вывести сообщение в таком формате:
# The PC "<имя ПК>" receive message from service "<имя сервиса>" what says "<сообщение>" because "<причина ошибки>"
# at <дата, время>

def parse_the_log_string(string: str) -> dict:

    result: dict = {}

    result["month"], result["day"], result["time"], result["pc_name"], service = string.split(" ", 4)
    result["service_name"], result["message"], result["result"] = service.split(": ")

    return result


def main():

    first_string: str = 'May 24 12:48:31 ideapad systemd[1]: logrotate.service: Succeeded.'
    second_string: str = 'May 24 14:03:01 ideapad colord[844]: failed to get session [pid 8279]: Нет доступных данных'

    parsed_string = parse_the_log_string(first_string)

    print(f"1. Обрабатываем строку '{first_string}'")
    print(f"\t1.1. {parsed_string['day']} {parsed_string['month']}, {parsed_string['time']}")
    print(f"\t1.2. {parsed_string['service_name']}")
    print("\t1.3.", first_string.replace(parsed_string['pc_name'], "PC-12092"))
    print("\t1.4.", first_string.find('failed'))
    print("\t1.5.", first_string.lower().count('s'))

    hours, minutes, seconds = parsed_string['time'].split(":")

    print("\t1.6.", int(hours)+int(minutes)+int(seconds))

    new_parsed_string = parse_the_log_string(second_string)

    print(f"2. Обрабатываем строку '{second_string}'")
    print(f'The PC \"{new_parsed_string["pc_name"]}\" receive message from service '
          f'\"{new_parsed_string["service_name"]}\" what says '
          f'\"{new_parsed_string["message"]}\" because '
          f'\"{new_parsed_string["result"]}\" at '
          f'{new_parsed_string["month"]} {new_parsed_string["day"]} {new_parsed_string["time"]}')


if __name__ == '__main__':
    main()
