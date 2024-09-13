import paramiko

# Функция для выполнения команд на удалённом сервере
def execute_remote_command(client, command):
    stdin, stdout, stderr = client.exec_command(command)
    output = stdout.read().decode()
    error = stderr.read().decode()

    if error:
        print(f"Error: {error.strip()}")
    else:
        print(f"Output:\n{output.strip()}")

# Функция для загрузки и выполнения скрипта
def upload_and_execute_script(host_info, key_filename, local_script, remote_script, bash_command=None):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Подключение с использованием ключа или логина и пароля
        if host_info.get('username') and host_info.get('password'):
            client.connect(host_info['host'], username=host_info['username'], password=host_info['password'], port=host_info['port'])
        else:
            client.connect(host_info['host'], username=host_info.get('username'), key_filename=key_filename, port=host_info['port'])

        if bash_command:
            # Выполнение команды напрямую
            print(f"Executing command on {host_info['host']}:{host_info['port']}...")
            execute_remote_command(client, bash_command)
        elif local_script and remote_script:
            # Открытие sftp-сессии
            sftp = client.open_sftp()

            # Загрузка bash-скрипта на удалённый сервер
            print(f"Uploading script to {host_info['host']}:{remote_script}...")
            sftp.put(local_script, remote_script)

            # Установка прав на выполнение скрипта
            execute_remote_command(client, f"chmod +x {remote_script}")

            # Выполнение скрипта
            print(f"Executing script on {host_info['host']}:{host_info['port']}...")
            execute_remote_command(client, f"bash {remote_script}")

            # Удаление скрипта с удалённого сервера
            execute_remote_command(client, f"rm -f {remote_script}")

            sftp.close()
        else:
            print("No script or command specified to execute.")
    except Exception as e:
        print(f"Failed on {host_info['host']}:{host_info['port']}: {e}")
    finally:
        client.close()
