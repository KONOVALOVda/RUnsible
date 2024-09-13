import paramiko

# Функция для выполнения команд на удалённом сервере
def execute_remote_command(client, command):
    stdin, stdout, stderr = client.exec_command(command)
    output = stdout.read().decode()
    error = stderr.read().decode()

    return output.strip(), error.strip()

# Функция для загрузки и выполнения скрипта
def upload_and_execute_script(host_info, default_key_filename, local_script, remote_script, bash_command=None):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    host_logs = []

    try:
        # Определяем SSH-ключ для подключения
        ssh_key = host_info.get('ssh_key', default_key_filename)

        # Подключение с использованием ключа или логина и пароля
        if host_info.get('username') and host_info.get('password'):
            client.connect(
                hostname=host_info['host'],
                username=host_info['username'],
                password=host_info['password'],
                port=host_info['port']
            )
        else:
            client.connect(
                hostname=host_info['host'],
                username=host_info.get('username'),
                key_filename=ssh_key,
                port=host_info['port']
            )

        if bash_command:
            # Выполнение команды напрямую
            host_logs.append(f"Executing command on {host_info['host']}:{host_info['port']}...")
            output, error = execute_remote_command(client, bash_command)
            if error:
                host_logs.append(f"Error: {error}")
            else:
                host_logs.append(f"Output:\n{output}")
        elif local_script and remote_script:
            # Открытие sftp-сессии
            sftp = client.open_sftp()

            # Загрузка bash-скрипта на удалённый сервер
            host_logs.append(f"Uploading script to {host_info['host']}:{remote_script}...")
            sftp.put(local_script, remote_script)

            # Установка прав на выполнение скрипта
            output, error = execute_remote_command(client, f"chmod +x {remote_script}")
            if error:
                host_logs.append(f"Error: {error}")
            else:
                if output:
                    host_logs.append(output)

            # Выполнение скрипта
            host_logs.append(f"Executing script on {host_info['host']}:{host_info['port']}...")
            output, error = execute_remote_command(client, f"bash {remote_script}")
            if error:
                host_logs.append(f"Error: {error}")
            else:
                host_logs.append(f"Output:\n{output}")

            # Удаление скрипта с удалённого сервера
            execute_remote_command(client, f"rm -f {remote_script}")

            sftp.close()
        else:
            host_logs.append("No script or command specified to execute.")
    except Exception as e:
        host_logs.append(f"Failed on {host_info['host']}:{host_info['port']}: {e}")
    finally:
        client.close()

    # Возвращаем логи для этого хоста
    return host_info['host'], host_logs
