import argparse
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
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

    # Создаём директорию для логов, если она не существует
    log_dir = os.path.join(SCRIPT_DIR, 'tmp')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Формируем имя файла лога с текущей датой
    date_str = datetime.now().strftime('%Y%m%d%H%M%S')
    log_file_path = os.path.join(log_dir, f'.log{date_str}.log')

    # Словарь для хранения логов от каждого хоста
    host_logs_dict = {}

    # Проходим по каждому хосту в группе и создаём задачи для пула потоков
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_host = {
            executor.submit(
                upload_and_execute_script,
                host_info,
                args.key,
                local_script_path,
                remote_script_path,
                bash_command=args.bash
            ): host_info for host_info in selected_hosts
        }

        for future in as_completed(future_to_host):
            host_info = future_to_host[future]
            host = host_info['host']
            try:
                host_name, host_logs = future.result()
                host_logs_dict[host_name] = host_logs
            except Exception as exc:
                print(f"[{host}] Generated an exception: {exc}")

    # Пишем логи в файл и выводим на консоль
    with open(log_file_path, 'w') as log_file:
        for host in sorted(host_logs_dict.keys()):
            log_file.write(f"=== Logs for {host} ===\n")
            log_file.write('\n'.join(host_logs_dict[host]))
            log_file.write('\n\n')

    # Выводим содержимое лога на консоль
    with open(log_file_path, 'r') as log_file:
        print(log_file.read())

if __name__ == '__main__':
    main()
