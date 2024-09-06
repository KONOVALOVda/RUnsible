import paramiko
import argparse
import os

default_ssh_port = 22  # Порт по умолчанию

# Путь к файлу с хостами
HOSTS_FILE = './hosts'

# Путь к локальному bash-скрипту
LOCAL_BASH_SCRIPT = './script.sh'
# Путь на удалённом сервере, куда будет загружен скрипт
REMOTE_BASH_SCRIPT = '/tmp/script.sh'

# Функция для чтения списка хостов из файла
def read_hosts(fhosts):
    hosts = {}
    current_group = None

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
                host_info = {}
                parts = line.split()
                host_port = parts[0]
                
                # Разделяем хост и порт, если указан
                if ':' in host_port:
                    host, port = host_port.split(':')
                    host_info['host'] = host
                    host_info['port'] = int(port)
                else:
                    host_info['host'] = host_port
                    host_info['port'] = default_ssh_port

                # Чтение runsible_user и runsible_password
                for part in parts[1:]:
                    if part.startswith('runsible_user='):
                        host_info['username'] = part.split('=')[1]
                    if part.startswith('runsible_password='):
                        host_info['password'] = part.split('=')[1]

                # Добавляем хост в текущую группу
                hosts[current_group].append(host_info)

    return hosts

# Функция для выполнения команд на удалённом сервере
def execute_remote_command(client, command):
    stdin, stdout, stderr = client.exec_command(command)
    output = stdout.read().decode()
    error = stderr.read().decode()

    if error:
        print(f"Error: {error}")
    else:
        print(f"Output: {output}")

# Функция для загрузки bash-скрипта, его выполнения и удаления
def upload_and_execute_script(host_info, key_filename):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Подключение с использованием ключа или логина и пароля
        if host_info.get('username') and host_info.get('password'):
            client.connect(host_info['host'], username=host_info['username'], password=host_info['password'], port=host_info['port'])
        else:
            client.connect(host_info['host'], username=host_info.get('username'), key_filename=key_filename, port=host_info['port'])

        # Открытие sftp-сессии
        sftp = client.open_sftp()

        # Загрузка bash-скрипта на удалённый сервер
        sftp.put(LOCAL_BASH_SCRIPT, REMOTE_BASH_SCRIPT)

        # Выполнение скрипта
        print(f"Executing script on {host_info['host']}:{host_info['port']}...")
        execute_remote_command(client, f"bash {REMOTE_BASH_SCRIPT}")

        # Удаление скрипта с удалённого сервера
        execute_remote_command(client, f"rm -f {REMOTE_BASH_SCRIPT}")

    except Exception as e:
        print(f"Failed on {host_info['host']}:{host_info['port']}: {e}")
    finally:
        client.close()

# Основная функция
def main():
    # Парсинг аргументов командной строки
    parser = argparse.ArgumentParser(description="Execute bash script on remote servers.")
    parser.add_argument('--key', help='Path to private SSH key for authentication', default=os.path.expanduser('~/.ssh/id_rsa'))
    parser.add_argument('--group', help='Group of hosts to connect', default='all')
    parser.add_argument('--hosts', help='Path to hosts file', default=HOSTS_FILE)

    args = parser.parse_args()

    # Чтение списка хостов и групп
    hosts_by_group = read_hosts(args.hosts)

    # Получение списка всех хостов для выбранной группы
    if args.group in hosts_by_group:
        selected_hosts = hosts_by_group[args.group]
    else:
        selected_hosts = []

    # Проходим по каждому хосту в группе
    for host_info in selected_hosts:
        print(f"Connecting to {host_info['host']} on port {host_info['port']}...")
        upload_and_execute_script(host_info, args.key)

if __name__ == '__main__':
    main()
