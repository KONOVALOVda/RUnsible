import os
import sys
import re

default_ssh_port = 22  # Порт по умолчанию

# Функция для расширения диапазона хостов
def expand_host_range(host_pattern):
    # Регулярное выражение для совпадения с паттернами {start:end} и {start..end}
    match = re.match(r'(.*){(\d+)([:\.]{1,2})(\d+)}(.*)', host_pattern)
    if match:
        prefix = match.group(1)
        start = int(match.group(2))
        sep = match.group(3)
        end = int(match.group(4))
        suffix = match.group(5)
        hosts = []
        for i in range(start, end + 1):
            hosts.append(f"{prefix}{i}{suffix}")
        return hosts
    else:
        return [host_pattern]

# Функция для чтения списка хостов из файла
def read_hosts(fhosts):
    print(f"Attempting to read hosts file from: {fhosts}")
    hosts = {}
    current_group = None

    try:
        with open(fhosts, 'r') as file:
            for line in file:
                line = line.strip()

                # Пропускаем пустые строки и комментарии
                if not line or line.startswith('#'):
                    continue

                # Если строка обозначает группу (начинается и заканчивается квадратными скобками)
                if line.startswith('[') and line.endswith(']'):
                    current_group = line[1:-1]  # Название группы
                    if current_group not in hosts:
                        hosts[current_group] = []
                    continue

                # Если это строка с хостом
                if current_group:
                    parts = line.split()
                    host_port = parts[0]
                    # Расширяем диапазоны хостов
                    expanded_hosts = expand_host_range(host_port)

                    # Чтение параметров после имени хоста
                    params = parts[1:]

                    for host_entry in expanded_hosts:
                        host_info = {}
                        # Разделяем хост и порт, если указан
                        if ':' in host_entry:
                            host, port = host_entry.split(':')
                            host_info['host'] = host
                            host_info['port'] = int(port)
                        else:
                            host_info['host'] = host_entry
                            host_info['port'] = default_ssh_port

                        # Чтение параметров хоста
                        for part in params:
                            if '=' in part:
                                key, value = part.split('=', 1)
                                if key in ['runsible_user', 'ansible_user']:
                                    host_info['username'] = value
                                elif key in ['runsible_password', 'ansible_password']:
                                    host_info['password'] = value
                                elif key in ['runsible_ssh_key', 'ansible_ssh_private_key_file']:
                                    host_info['ssh_key'] = os.path.expanduser(value)

                        # Добавляем хост в текущую группу
                        hosts[current_group].append(host_info)

        return hosts
    except FileNotFoundError:
        print(f"Error: Hosts file not found at {fhosts}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred while reading hosts file: {e}")
        sys.exit(1)
