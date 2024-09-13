import argparse
import os
import sys
from threading import Thread
from inventory import read_hosts
from playbook import upload_and_execute_script

# Путь к SSH-ключу по умолчанию
DEFAULT_SSH_KEY = os.path.expanduser('~/.ssh/id_rsa')

# Путь к файлу с хостами по умолчанию
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_HOSTS_FILE = os.path.join(SCRIPT_DIR, 'hosts')

def main():
    # Парсинг аргументов командной строки
    parser = argparse.ArgumentParser(description="Execute bash script on remote servers.")
    parser.add_argument('-key', help='Path to private SSH key for authentication', default=DEFAULT_SSH_KEY)
    parser.add_argument('-group', help='Group of hosts to connect', default='all')
    parser.add_argument('-i', help='Path to hosts inventory file', default=DEFAULT_HOSTS_FILE)
    parser.add_argument('-bash', help='Execute bash command directly on remote hosts')
    parser.add_argument('-sh', help='Path to local bash script to execute on remote hosts')
    parser.add_argument('-remote_path', help='Path on remote host where script will be uploaded', default='/tmp')

    args = parser.parse_args()

    # Чтение списка хостов и групп
    hosts_by_group = read_hosts(args.i)

    # Получение списка всех хостов для выбранной группы
    if args.group in hosts_by_group:
        selected_hosts = hosts_by_group[args.group]
    else:
        print(f"Group '{args.group}' not found in hosts file.")
        sys.exit(1)

    # Настройка путей скрипта, если указана опция -sh
    if args.sh:
        local_script_path = os.path.abspath(args.sh)
        if not os.path.isfile(local_script_path):
            print(f"Local script '{local_script_path}' not found.")
            sys.exit(1)
        script_name = os.path.basename(local_script_path).lstrip('/')
        remote_script_path = f"{args.remote_path.rstrip('/')}/{script_name}"
    else:
        local_script_path = None
        remote_script_path = None

    threads = []

    # Проходим по каждому хосту в группе и создаём поток
    for host_info in selected_hosts:
        print(f"Scheduling connection to {host_info['host']} on port {host_info['port']}...")
        thread = Thread(
            target=upload_and_execute_script,
            args=(
                host_info,
                args.key,
                local_script_path,
                remote_script_path,
            ),
            kwargs={'bash_command': args.bash}
        )
        threads.append(thread)
        thread.start()

    # Ожидаем завершения всех потоков
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()
