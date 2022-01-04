import json
import os
import time
from dataclasses import dataclass
import logging
import requests as requests
import psutil


class PerfMon:
    _logger: logging.Logger = None
    _is_initiated: bool = False
    _host_information = None
    _network_information = None
    _disk_information = None
    _memory_information = None
    _cpu_information = None
    _load_average = None

    @dataclass()
    class CPUInformation:
        cpu_cores: int = psutil.cpu_count()
        cpu_physical_cores: int = psutil.cpu_count(logical=False)
        cpu_frequency: dict[str, float] = None

        def __post_init__(self):
            try:
                cpu_info = psutil.cpu_freq()
                self.cpu_frequency = {'current': cpu_info.current, 'min': cpu_info.min, 'max': cpu_info.max}
            except FileNotFoundError as exc:
                print(f"Cannot recognize your processor speed: {exc}")
                self.cpu_frequency = {'current': 0.0, 'min': 0.0, 'max': 0.0}

        def __str__(self):
            return f'CPU Information:' \
                   f'\n\tTotal cores: {self.cpu_cores}' \
                   f'\n\tPhysical cores: {self.cpu_physical_cores}' \
                   f'\n\tFrequency: {self.cpu_frequency}'

        def get_info(self):
            return [{
                'cpu_cores': self.cpu_cores,
                'cpu_physical_cores': self.cpu_physical_cores,
                'cpu_frequency_current': self.cpu_frequency['current'],
                'cpu_frequency_minimum': self.cpu_frequency['min'],
                'cpu_frequency_maximum': self.cpu_frequency['max'],
            }, ]

    @dataclass()
    class DiskInformation:
        partitions = psutil.disk_partitions()

        def __str__(self):
            value = 'Disks information:'

            for partition in self.partitions:
                disk_usage = psutil.disk_usage(partition.mountpoint)

                value += f'\n\tDisk name: {partition.device:>15}' \
                         f'\tMount point: {partition.mountpoint: >30}' \
                         f'\tFile System Type: {partition.fstype: ^6}' \
                         f'\tTotal space: {disk_usage.total:>20d}' \
                         f'\tUsed space: {disk_usage.used:>20d}'

            return value

        def get_info(self):
            value = []

            for partition in self.partitions:
                disk_usage = psutil.disk_usage(partition.mountpoint)

                value.append(
                    {
                        'disk_name': partition.device,
                        'mount_point': partition.mountpoint,
                        'file_system_type': partition.fstype,
                        'total': disk_usage.total,
                        'used': disk_usage.used,
                     })

            return value

    @dataclass()
    class HostInformation:
        sys_name: str = psutil.users()[0].name
        host_name: str = psutil.users()[0].host if psutil.users()[0].host else 'localhost'

        def get_info(self):
            return [{'sys_name': self.sys_name, 'host_name': self.host_name}, ]

        def __str__(self):
            return f"Host information:\n\tSystem name: {self.sys_name}\n\tHost name: {self.host_name}"

    @dataclass()
    class LoadAverage:
        load_average: tuple = psutil.getloadavg()
        one_minute: float = load_average[0]
        five_minutes: float = load_average[1]
        fifteen_minutes: float = load_average[2]

        def get_info(self):
            return [{'one_minute': self.one_minute,
                     'five_minutes': self.five_minutes,
                     'fifteen_minutes': self.fifteen_minutes},
                    ]

        def __str__(self):
            return f'Average load:' \
                   f'\n\t1 min. - {self.one_minute}' \
                   f'\n\t5 min. - {self.five_minutes}' \
                   f'\n\t15 min. - {self.fifteen_minutes}'

    @dataclass()
    class MemoryInformation:
        memory_info = psutil.virtual_memory()
        memory_total: float = memory_info.total
        memory_used: float = memory_info.used
        memory_percent: float = memory_info.percent

        def get_info(self):
            return [{
                'total': self.memory_total,
                'used': self.memory_used,
                'percent': self.memory_percent,
                    }, ]

        def __str__(self):
            return f"Memory info:" \
                   f"\n\tMemory total: {self.memory_total}" \
                   f"\n\tMemory used: {self.memory_used}" \
                   f"\n\tMemory percent: {self.memory_percent}"

    @dataclass()
    class NetworkInformation:
        network_information = psutil.net_if_stats()

        def get_info(self):
            value = []

            for interface, status in self.network_information.items():
                value.append({'interface': interface, 'status': status.isup, 'mtu': status.mtu})

            return value

        @staticmethod
        def get_status(status: bool):
            return "Up" if status else "Down"

        def __str__(self):
            value = 'Network information:'

            for interface, status in self.network_information.items():
                value += f'\n\tInterface: {interface:>8} ' \
                         f'\tStatus: {self.get_status(status.isup):^4}' \
                         f'\tMTU: {status.mtu:>7}'

            return value

    def __init__(self, logger: logging.Logger = None):

        self._logger = logger
        # self.init()

    def init(self):
        self._logger.info("Getting information about host ...")
        self.host_information = self.HostInformation()

        self._logger.info("Getting information about average loading ...")
        self.load_average = self.LoadAverage()

        self._logger.info("Getting memory information ...")
        self.memory_information = self.MemoryInformation()

        self._logger.info('Getting information about network configuration ...')
        self.network_information = self.NetworkInformation()

        self._logger.info('Getting disks information ...')
        self.disk_information = self.DiskInformation()

        self._logger.info('Getting information about CPU ...')
        self.cpu_information = self.CPUInformation()

        self._is_initiated = True

    def __str__(self):
        if not self._is_initiated:
            self.init()

        return f"Performance Information:" \
               f"\n{self.host_information}" \
               f"\n{self.network_information}" \
               f"\n{self.disk_information}" \
               f"\n{self.memory_information}" \
               f"\n{self.cpu_information}" \
               f"\n{self.load_average}"

    def get_info(self):
        if not self._is_initiated:
            self.init()

        return {
            'host_information': self.host_information.get_info(),
            'network_information': self.network_information.get_info(),
            'disk_information': self.disk_information.get_info(),
            'memory_information': self.memory_information.get_info(),
            'cpu_information': self.cpu_information.get_info(),
            'load_average': self.load_average.get_info(),
        }

    @property
    def cpu_information(self):
        return self._cpu_information

    @cpu_information.setter
    def cpu_information(self, value):
        self._cpu_information = value

    @property
    def disk_information(self):
        return self._disk_information

    @disk_information.setter
    def disk_information(self, value):
        self._disk_information = value

    @property
    def network_information(self):
        return self._network_information

    @network_information.setter
    def network_information(self, value):
        self._network_information = value

    @property
    def host_information(self):
        return self._host_information

    @host_information.setter
    def host_information(self, value):
        self._host_information = value

    @property
    def load_average(self):
        return self._load_average

    @load_average.setter
    def load_average(self, value):
        self._load_average = value

    @property
    def memory_information(self):
        return self._memory_information

    @memory_information.setter
    def memory_information(self, value):
        self._memory_information = value


class Executor:
    _external_ip_address: str = ''
    _server: dict = None
    _logger: logging.Logger = None
    _perf_mon_log: PerfMon = None

    def __init__(self, perf_mon_log: PerfMon, srv: dict = None, logger: logging.Logger = None):

        if logger:
            self._logger = logger
        else:
            self.init_logger()
            self._logger.warning("Logger wasn't provided. Default logger has been initiated.")

        if perf_mon_log:
            self._perf_mon_log = perf_mon_log
        else:
            self._logger.error("Cannot run Executor! Performance monitor isn't assigned.")
            return

        if srv:
            self._server = srv
        else:
            self._logger.warning("Server isn't assigned. Default taken.")
            self._server = {'address': 'localhost', 'port': 8000}

        try:
            self._logger.info("Getting information about external IP address...")
            self._external_ip_address = requests.get('https://api.my-ip.io/ip').text
        except requests.exceptions.RequestException as exc:
            self._logger.error(f'Cannot resolve the external IP address - {exc}')

        if self.is_server_exist():
            self._logger.info('Host already in the list')
        else:
            self._logger.info('Host not in the list. Adding into it ...')

            try:
                description = os.environ["DESC"]
            except KeyError:
                description = 'My personal PC'

            data = {'ip_address': self._external_ip_address,
                    'description': description,
                    'name': self._perf_mon_log.HostInformation().host_name,
                    'server_is_active': True}

            self.dump_data(uri='/api/servers/add', data=json.dumps(data))

    def dump_data(self, uri: str, data):
        try:
            self._logger.info(f"Dumping data into the server {self._server}")

            headers = {'Content-type': 'application/json'}
            response = requests.post(url=f'http://{self._server["address"]}:{self._server["port"]}{uri}',
                                     data=data,
                                     headers=headers)

        except requests.exceptions.RequestException as exc:
            self._logger.error(f"Cannot dump data into the server {self._server}: {exc}")
            return False

        if response.status_code == 201:
            self._logger.info("Successful!!!")
            return True
        else:
            self._logger.info("Failed.")
            return False

    def is_server_exist(self) -> bool:

        self._logger.info("Checking the existence of server in the list...")
        try:
            response = requests.get(f'http://{self._server["address"]}:{self._server["port"]}/api/servers/')

            if self._external_ip_address and self._external_ip_address in \
                    [host['ip_address'] for host in response.json()]:
                return True

        except requests.exceptions.RequestException as exc:
            self._logger.error(f"DRW isn't accessible: {exc}")

        return False

    def init_logger(self) -> bool:

        self._logger = logging.getLogger("Internal Logger")
        self._logger.setLevel(logging.INFO)
        log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%b %d %H:%M:%S')

        handler = logging.StreamHandler()
        handler.setFormatter(log_formatter)
        handler.setLevel(logging.INFO)

        self._logger.addHandler(handler)

        return True

    def run(self):

        while True:
            self._perf_mon_log.init()
            self.dump_data(uri='/api/perfmon/add/', data=json.dumps(self._perf_mon_log.get_info()))
            time.sleep(60)


if __name__ == '__main__':

    server = {'address': 'localhost', 'port': 8000}

    monitor_log = logging.getLogger(__name__)
    monitor_log.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%b %d %H:%M:%S')

    file_log_handler = logging.FileHandler('log_file.log', 'w', 'utf-8')
    file_log_handler.setFormatter(formatter)
    file_log_handler.setLevel(logging.INFO)

    log_handler = logging.StreamHandler()
    log_handler.setFormatter(formatter)
    log_handler.setLevel(logging.INFO)

    monitor_log.addHandler(log_handler)
    monitor_log.addHandler(file_log_handler)

    monitor_log.info("The programme is started.")
    perf_mon = PerfMon(logger=monitor_log)
    executor = Executor(perf_mon_log=perf_mon, srv=server, logger=monitor_log)
    executor.run()

