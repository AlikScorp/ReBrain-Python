from os import getlogin
from psutil import virtual_memory

username: str = getlogin()
memory_information = virtual_memory()

general_information: dict = {
    'user_name': username,
    'memory_total': memory_information.total,
    'memory_available': memory_information.available,
    'memory_percent': memory_information.percent,
    'memory_used': memory_information.used,
    'memory_free': memory_information.free,
}

if __name__ == "__main__":
    print(general_information)
