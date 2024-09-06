#include <libssh/libssh.h>
#include <iostream>

int execute_ssh_command(const std::string& host, const std::string& user, const std::string& password, const std::string& command) {
    ssh_session session = ssh_new();
    if (session == nullptr) return -1;

    ssh_options_set(session, SSH_OPTIONS_HOST, host.c_str());
    ssh_options_set(session, SSH_OPTIONS_USER, user.c_str());
    
    int rc = ssh_connect(session);
    if (rc != SSH_OK) {
        ssh_free(session);
        return -2;
    }

    rc = ssh_userauth_password(session, nullptr, password.c_str());
    if (rc != SSH_AUTH_SUCCESS) {
        ssh_disconnect(session);
        ssh_free(session);
        return -3;
    }

    ssh_channel channel = ssh_channel_new(session);
    if (channel == nullptr) {
        ssh_disconnect(session);
        ssh_free(session);
        return -4;
    }

    rc = ssh_channel_open_session(channel);
    if (rc != SSH_OK) {
        ssh_channel_free(channel);
        ssh_disconnect(session);
        ssh_free(session);
        return -5;
    }

    rc = ssh_channel_request_exec(channel, command.c_str());
    if (rc != SSH_OK) {
        ssh_channel_close(channel);
        ssh_channel_free(channel);
        ssh_disconnect(session);
        ssh_free(session);
        return -6;
    }

    // Read output (if necessary)
    char buffer[256];
    int nbytes;
    while ((nbytes = ssh_channel_read(channel, buffer, sizeof(buffer), 0)) > 0) {
        std::cout.write(buffer, nbytes);
    }

    // Sending a command to delete the script (additional implementation required)

    ssh_channel_send_eof(channel);
    ssh_channel_close(channel);
    ssh_channel_free(channel);
    ssh_disconnect(session);
    ssh_free(session);

    return 0;
}

int main() {
    std::string host = "example.com";
    std::string user = "username";
    std::string password = "password";
    std::string command = "bash your_script.sh; rm your_script.sh";

    int result = execute_ssh_command(host, user, password, command);
    if (result == 0) {
        std::cout << "Command executed successfully." << std::endl;
    } else {
        std::cout << "Error executing command: " << result << std::endl;
    }

    return 0;
}
