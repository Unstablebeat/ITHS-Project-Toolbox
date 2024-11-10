# Project Toolbox
This toolbox contains 3 different tools written in Python and is designed for penetration testing and to find potential security risks.  
All the tools can be used from `toolbox.py`.
- ***Port scanner***  
- ***Cryptotool***
- ***SSH Automation***
#### Installation
1. Clone this repo to your local machine.  
```git clone https://github.com/Unstablebeat/ITHS-Project-Toolbox.git```
2. Install the required libraries  
```pip install -r requirements.txt```
**Note:** To use port scanner you need to have nmap installed, you can download [Nmap](https://nmap.org/download) here
## Usage
### 1. *Using port scanner*  

To start use `python toolbox.py scanner -h` to see our options  
```
usage: toolbox.py scanner [-h] [-m ipfile.txt] [-s save.txt] [-os | -c custom] [target]

positional arguments:
  target         To scan multiple ip's use -m

options:
  -h, --help     show this help message and exit
  -m ipfile.txt  Scan a list of ip's in a file
  -s save.txt    Used to save scanner output to file
  -os            Used to scan for os
  -c custom      Enter custom nmap flags(e.g ' -sV -Pn -p')
```
- We have the choice to scan a single ip-adress or multiple ip's given in a .txt file  
- Save the output of the scan to a file  
- Do a OS-Scan to see the most likely operating system  
- Use custom nmap flags (Altho the output will still be Hoststatus, Protocol, Ports and services)  

A few examples:  
`python toolbox.py scanner 192.168.1.1 -s savefile.txt`  
`python toolbox.py scanner -m targets.txt -os`  
`python toolbox.py scanner -m targets.txt -s savefile.txt -c '-Pn -T4'`  
`python toolbox.py scanner 192.168.1.1 -c ' -T4'`  
**NOTE:** I've noticed that when using the -c flag a space is needed  
after the first > ' < if only passing in one flag.  

#### Example output from just providing an IP:
```
----------------------------------
Host: 255.255.255.0
State: up
Protocol: tcp
Port: 22, State: open, Service: SSH
```

### 2. *Using cryptotool*
To start use `python toolbox.py crypto -h` to see our options  
```
usage: toolbox.py crypto [-h] [-s save.txt] [-d File Key | -e File Key | -g [save.txt]]

options:
  -h, --help     show this help message and exit
  -s save.txt    Used with decryption to save output to file
  -d File Key    For Decryption add File and Key
  -e File Key    For Encryption add File and Key
  -g [save.txt]  Optional, enter a name for key-file
```  
- We have the choice to either Encrypt / Decrypt a file or generate a key.  
- When encrypting a file it will replace the original file with a new one ending in .enc
- By default Decryption will print out into the terminal, if we want to save the output to a file we use -s savefile.txt.
 
#### A few examples with output:  
`python toolbox.py crypto -g`  
**WARNING:** Running this twice will overwrite the first default.key and the same key used for encryption is needed to decrypt!
```
python toolbox.py crypto -g
---------------------------------
Key saved as: default.key
Key: Tv_gi4t19-Bl0-7b7ZhYA9axMt08K7Bgl0nnEO2qbmc=
```

<hr>

`python toolbox.py crypto -g my`  
```
python toolbox.py crypto -g my
---------------------------------
Key saved as: my.key
Key: 6WOQCRCeinqP8KyfsJSKf-jbFSy2CCe8EDUovX5pglc=
```

<hr>

`python toolbox.py crypto -e yourfile.txt default.key`
```
python toolbox.py crypto -e test.txt default.key
-------------------------------------
Key: Tv_gi4t19-Bl0-7b7ZhYA9axMt08K7Bgl0nnEO2qbmc=
-------------------------------------
Encrypted text: b'gAAAAABnIhOnWcNJAIBbV31nIKzB75-B_g9WgzV8GY5DqSZGx_iUofXaSgRlo5X_Y-H3S8cUAG-lauDdTT6Ec6GmZ1BRGf5ycA=='
-------------------------------------
File: test.txt > test_txt.enc
```

<hr>

`python toolbox.py crypto -d yourfile.enc default.key`
```
python toolbox.py crypto -d test_txt.enc default.key
-------------------------------------
Key: Tv_gi4t19-Bl0-7b7ZhYA9axMt08K7Bgl0nnEO2qbmc=
-------------------------------------
Decrypted text:
This is a test!
-------------------------------------
```

<hr>

`python toolbox.py crypto -d yourfile.txt default.key -s savefile.txt`
```
python toolbox.py crypto -d test_txt.enc default.key -s test.txt
-------------------------------------
Key: Tv_gi4t19-Bl0-7b7ZhYA9axMt08K7Bgl0nnEO2qbmc=
-------------------------------------
Decrypted text:
This is a test!
-------------------------------------

Decryption saved as a copy: test.txt
```

### 3. *Using SSH Automation*
To start use `python toolbox.py ssh -h` to see our options

```
python toolbox.py ssh -h                                                                             
usage: toolbox.py ssh [-h] [-u l_File r_Path] [-a] [-d l_path r_path] [-s] [-b passwordlist | -bup users passwords | -bd passwords l_path r_path | -bu passwords l_path r_path | -c commandfile]
                      ip [username] [password]

positional arguments:
  ip                    Enter ip for ssh-connection
  username              Enter username for ssh-connection unless -bu is used
  password              Enter password for ssh-connection unless -b/-bu/-bg is used

options:
  -h, --help            show this help message and exit
  -u l_File r_Path      Upload local file/s to remote path
  -a                    If used, targets all files in a dir
  -d l_path r_path      Download file/s to local path from remote path
  -s                    Used with bruteforce, enabels sleeptime after every 5 attempts
  -b passwordlist       Bruteforce password, submit passwordlist
  -bup users passwords  Bruteforce username and password, submit user and passwordlists
  -bd passwords l_path r_path
                        Bruteforce password and download files from a list.txt
  -bu passwords l_path r_path
                        Bruteforce password and uploads files from a list.txt
  -c commandfile        To run commands after connection from a file
```

- Upload a specific file.
- Upload everything in a folder, including subfolders with the -a flag.
- Download a specific file.
- Download everything in a folder, including subfolders with the -a flag.
- Bruteforce ssh password.
- Bruteforce ssh username and password.
- Bruteforce ssh password aswell as grabing predetermined files submitted via .txt file.
- Bruteforce ssh password aswell as uploading predetermined files submitted via .txt file.
- Connect via ssh and run commands submitted via .txt file.

#### A few examples with output:  

`Python toolbox.py ssh ip username password -u C:\Path\to\local\file.txt /Path/to/remote/file.txt`

```
python toolbox.py ssh 192.168.1.1 kali kali -u D:\Python\Misc\test.txt /home/kali/Documents/remote_test.txt
Connected to 192.168.1.1 as kali
The file: D:\Python\Misc\test.txt has been uploaded to /home/kali/Documents/remote_test.txt
```
***Note:*** If the file you wish to upload/(download path) is in the same directory as the script you do not need to specify the path  
(e.g `-u test.txt /home/kali/Documents/remote_test.txt`)


<hr>


`Python toolbox.py ssh ip username password -d C:\Path\to\local\folder /Path/to/remote/folder -a`
```
python toolbox.py ssh 192.168.1.1 kali kali -d D:\Python\Misc /home/kali/Documents -a                
Connected to 192.168.1.1 as kali
The file: /home/kali/Documents/remote_test.txt has been downloaded to D:\Python\Misc\remote_test.txt
The file: /home/kali/Documents/hello.txt has been downloaded to D:\Python\Misc\hello.txt
The file: /home/kali/Documents/world.txt has been downloaded to D:\Python\Misc\world.txt
The file: /home/kali/Documents/A_folder/file_in_folder.txt has been downloaded to D:\Python\Misc\A_folder\file_in_folder.txt
```  


<hr>


`Python toolbox.py ssh ip username -b passwords.txt`
```
python toolbox.py ssh 192.168.1.1 kali -b passwords.txt
Trying to bruteforce password on 192.168.1.1 as kali
Trying kali-admin
Failed with kali - admin
----------------------------
Trying kali-password
Failed with kali - password
----------------------------
Trying kali-kali

----------------------------
Successful login with kali-kali
```


<hr>


`Python toolbox.py ssh ip username password -c commands.txt`  
***Note:*** The commands.txt only contains 'whoami' but you can have a file with multiple commands and it will execute them line by line
```
python toolbox.py ssh 192.168.1.1 kali kali -c commands.txt
Connected to 192.168.199.128 as kali
kali
```


<hr>


`Python toolbox.py ssh ip username -bup users.txt passwords.txt`
```
python toolbox.py ssh 192.168.1.1 -bup usernames.txt passwords.txt
Trying to bruteforce username and password on 192.168.1.1
Trying admin-admin
Failed with admin - admin
----------------------------
Trying admin-kali
Failed with admin - kali
----------------------------
Trying kali-admin
Failed with kali - admin
----------------------------
Trying kali-kali

----------------------------
Successful login with kali-kali
```

<hr>


`Python toolbox.py ssh ip username -bd passwords.txt C:\Path\to\local\folder files.txt`
```
python toolbox.py ssh 192.168.1.1 kali -bd passwords.txt D:\Python\Misc\ path.txt
Trying to bruteforce password on 192.168.1.1 as kali
Trying kali-admin
Failed with kali - admin
----------------------------
Trying kali-password
Failed with kali - password
----------------------------
Trying kali-kali

----------------------------
Successful login with kali-kali
----------------------------

Downloaded /etc/passwd to D:\Python\Misc\passwd
Error: Could not download ~/.zsh_history. Reason: [Errno 2] No such file
Downloaded /home/kali/Documents/test.txt to D:\Python\Misc\test.txt
Error: Could not download /etc/shadow. Reason: [Errno 13] Permission denied
```

<hr>

`Python toolbox.py ssh ip username -bu passwords.txt files.txt /path/to/upload`
```
python toolbox.py ssh 192.168.1.1 kali -bu passwords.txt test.txt /home/kali/Documents/test/
Trying to bruteforce password on 192.168.1.1 as kali
Trying kali-admin
Failed with kali - admin
----------------------------
Trying kali-password
Failed with kali - password
----------------------------
Trying kali-kali

----------------------------
Successful login with kali-kali
----------------------------

Uploaded D:\Test\test1.txt to /home/kali/Documents/test/test1.txt
Uploaded D:\test.txt to /home/kali/Documents/test/test.txt
```

### ***Final Note:*** The -s flag.
The -s flag is used in tandem with any of the bruteforce options, applying -s will put a timeout on the bruteforce if it fails 5 attempts without breaking the password, this will make bruteforceing username and password take a tremendous amount of time because the timeouts goes 1min -> 5min -> 10min -> 30min between attempts.   


## Contribution
To contribute
1. Fork this repo
2. Create a new branch for your feature
3. Submit a pull request when done

All contributions are welcome!
