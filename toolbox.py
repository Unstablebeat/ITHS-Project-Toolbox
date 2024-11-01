"""
argparse module providing the ability to take arguments in the commandline.

importing selfmade cryptotool, keygenerator, ssh and scan to call functions
"""
import argparse
import cryptotool
import keygenerator
import ssh
from scan import _scan, _scan_os

def cli():
    """Function for running the argparse commands"""
    parser = argparse.ArgumentParser(description="---Toolbox---",)

    subparser = parser.add_subparsers(dest="tool")
    nmap_parser = subparser.add_parser("scanner", help="'scanner -h' for more information")
    crypto_parser = subparser.add_parser("crypto", help="'crypto -h' for more information")
    ssh_parser = subparser.add_parser("ssh", help="'ssh -h' for more information")

    ssh_parser.add_argument("ip",help="Enter ip for ssh-connection")
    ssh_parser.add_argument("username",
                            nargs='?',
                            help="Enter username for ssh-connection unless -bu is used")

    ssh_parser.add_argument("password",
                            nargs='?',
                            help="Enter password for ssh-connection unless -b/-bu/-bg is used")

    ssh_parser.add_argument("-u",
                            dest="upload",
                            nargs=2,
                            metavar=("l_File", "r_Path"),
                            help="Upload local file/s to remote path")

    ssh_parser.add_argument("-a",
                            dest="all",
                            action="store_true",
                            help="If used, targets all files in a dir")

    ssh_parser.add_argument("-d",
                            dest="download",
                            nargs=2,
                            metavar=("l_path", "r_path"),
                            help="Download file/s to local path from remote path")

    ssh_parser.add_argument("-s",
                            dest="sleep",
                            action="store_true",
                            help="Used with bruteforce, enabels sleeptime after every 5 attempts")

    ssh_parser_group = ssh_parser.add_mutually_exclusive_group()
    ssh_parser_group.add_argument("-b",
                            dest="bf_password",
                            metavar="passwordlist",
                            help="Bruteforce password, submit passwordlist")

    ssh_parser_group.add_argument("-bup",
                            dest="bf_user_password",
                            nargs=2,
                            metavar=("users", "passwords"),
                            help="Bruteforce username and password, submit user and passwordlists")

    ssh_parser_group.add_argument("-bd",
                            dest="bf_password_downloadfiles",
                            nargs=3,
                            metavar=("passwords", "l_path", "r_path"),
                            help="Bruteforce password and download files from a list.txt")

    ssh_parser_group.add_argument("-bu",
                                dest="bf_password_uploadfiles",
                                nargs=3,
                                metavar=("passwords", "l_path", "r_path"),
                                help="Bruteforce password and uploads files from a list.txt")

    ssh_parser_group.add_argument("-c",
                            dest="command",
                            metavar="commandfile",
                            help="To run commands after connection from a file")


    nmap_parser.add_argument("target",
                             nargs='?',
                             help="To scan multiple ip's use -m")

    nmap_parser.add_argument("-m",
                             dest="multiple",
                             nargs=1,
                             metavar="ipfile.txt",
                             help="Scan a list of ip's in a file")

    nmap_parser.add_argument("-s",
                            dest="save",
                            metavar="save.txt",
                            help="Used to save scanner output to file")

    nmap_parser_group = nmap_parser.add_mutually_exclusive_group()
    nmap_parser_group.add_argument("-os",
                                   action="store_true",
                                   help="Used to scan for os")

    nmap_parser_group.add_argument("-c",
                                    dest="custom",
                                    metavar="custom",
                                    help="Enter custom nmap flags(e.g ' -sV -Pn -p')")
    #-c flag requires a space after the first ' if only one flag is submitted to run


    crypto_parser.add_argument("-s",
                                dest="save",
                                metavar="save.txt",
                                help="Used with decryption to save output to file")

    crypto_parser_group = crypto_parser.add_mutually_exclusive_group()
    crypto_parser_group.add_argument("-d",
                                    dest="decryption",
                                    nargs=2,
                                    metavar=("File", "Key"),
                                    help="For Decryption add File and Key")

    crypto_parser_group.add_argument("-e",
                                    dest="encryption",
                                    nargs=2,
                                    metavar=("File", "Key"),
                                    help="For Encryption add File and Key")

    crypto_parser_group.add_argument("-g",
                                    dest="generatekey",
                                    nargs='?',
                                    metavar="save.txt",
                                    const='default',
                                    help="Optional, enter a name for key-file")



    args = parser.parse_args()

    return args

def crypto(args):
    """Taking argparse input and calls the correct crypto function"""
    if args.generatekey:
        keygenerator.key_gen(args.generatekey)
    elif args.decryption:
        try:
            file, key = args.decryption
            if args.save:
                cryptotool.decrypt(file, key, args.save)
            else:
                cryptotool.decrypt(file, key)
        except FileNotFoundError as e:
            print(e)
    elif args.encryption:
        try:
            file, key = args.encryption
            cryptotool.encrypt(file, key)
        except FileNotFoundError as e:
            print(e)

def scanner(args):
    """Taking argparse input and calls the correct scanner function"""
    targets = []
    save_file = []

    if args.target:
        targets.append(args.target)

    if args.save:
        save_file = args.save

    if args.multiple:
        try:
            with open(args.multiple[0], 'r', encoding='UTF-8') as ip_file:
                targets = ip_file.read().splitlines()
        except FileNotFoundError as e:
            print(e)

    if args.os:
        _scan_os(targets, save_file)
    elif args.custom:
        _scan(targets, save_file, args.custom)
    else:
        _scan(targets, save_file)

def ssh_tool(args):
    """Taking argparse input and calls the correct ssh function"""
    ip = args.ip
    username = args.username
    pwd = args.password

    if args.download:
        if args.all:
            ssh.ssh_download(ip, username, pwd, args.download[0], args.download[1], True)
        else:
            ssh.ssh_download(ip, username, pwd, args.download[0], args.download[1])

    if args.upload:
        if args.all:
            ssh.ssh_upload(ip, username, pwd, args.upload[0], args.upload[1], True)
        else:
            ssh.ssh_upload(ip, username, pwd, args.upload[0], args.upload[1])

    if args.command:
        commands = args.command
        ssh.ssh_commands(ip, username, pwd, commands)

    if args.bf_password:
        passwords = args.bf_password
        if args.sleep:
            ssh.ssh_brute_password(ip, username, passwords, True)
        else:
            ssh.ssh_brute_password(ip, username, passwords)

    if args.bf_password_downloadfiles:
        passwords, local_path, remote_path = args.bf_password_downloadfiles
        if args.sleep:
            ssh.ssh_brute_grab(ip, username, passwords, local_path, remote_path, True)
        else:
            ssh.ssh_brute_grab(ip, username, passwords, local_path, remote_path)

    if args.bf_user_password:
        usernames, passwords = args.bf_user_password
        if args.sleep:
            ssh.ssh_brute_user_password(ip, usernames, passwords, True)
        else:
            ssh.ssh_brute_user_password(ip, usernames, passwords)

    if args.bf_password_uploadfiles:
        passwords, local_path, remote_path = args.bf_password_uploadfiles
        if args.sleep:
            ssh.ssh_brute_put(ip, username, passwords, local_path, remote_path, True)
        else:
            ssh.ssh_brute_put(ip, username, passwords, local_path, remote_path)

def main():
    """Mainscript for running the toolbox"""
    args = cli()

    if args.tool == "crypto":
        crypto(args)

    if args.tool == "scanner":
        scanner(args)

    if args.tool == "ssh":
        ssh_tool(args)

if __name__ == "__main__":
    main()
