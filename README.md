# Project Toolbox
This toolbox contains 3 different tools written in Python and is designed for penetration testing. All the tools can be used from `toolbox.py` or used individually.
- ***Port scanner***  
- ***Cryptotool***
- ***SSH Automation***
#### Installation
1. Clone this repo to your local machine.  
```git clone https://github.com/Unstablebeat/ITHS-Project-Toolbox.git```
2. Install the required libraries  
```pip install -r requirements.txt```
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

Example output from just providing an IP:
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
 
A few examples:  
`python toolbox.py crypto -g`  
**WARNING:** Running this twice will overwrite the first default.key and the same key used for encryption is needed to decrypt!
```
python toolbox.py crypto -g
---------------------------------
Key saved as: default.key
Key: Tv_gi4t19-Bl0-7b7ZhYA9axMt08K7Bgl0nnEO2qbmc=
```


`python toolbox.py crypto -g my`  
```
python toolbox.py crypto -g my
---------------------------------
Key saved as: my.key
Key: 6WOQCRCeinqP8KyfsJSKf-jbFSy2CCe8EDUovX5pglc=
```


`python toolbox.py crypto -e test.txt my.key`
```
python toolbox.py crypto -e test.txt default.key
-------------------------------------
Key: Tv_gi4t19-Bl0-7b7ZhYA9axMt08K7Bgl0nnEO2qbmc=
-------------------------------------
Encrypted text: b'gAAAAABnIhOnWcNJAIBbV31nIKzB75-B_g9WgzV8GY5DqSZGx_iUofXaSgRlo5X_Y-H3S8cUAG-lauDdTT6Ec6GmZ1BRGf5ycA=='
-------------------------------------
File: test.txt > test_txt.enc
```

`python toolbox.py crypto -d yourfile.txt default.key`
```
python toolbox.py crypto -d test_txt.enc default.key
-------------------------------------
Key: Tv_gi4t19-Bl0-7b7ZhYA9axMt08K7Bgl0nnEO2qbmc=
-------------------------------------
Decrypted text:
This is a test!
-------------------------------------
```

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

## Port scanner
A Simple Port Scanner using nmap. This tool os ised tp scan a network for open ports and identify potential security risks.
- ***Host-status***
- ***Open ports***
- ***Service***
- ***Operating-System***
- ***Optional nmap flags*** (Output will still only show host-status, ports and services)
#### Usage
text text text

## Cryptotool
A crypto-tool that can Encrypt and Decrypt files with a key that can also be generated with this tool
- ***Key Generator***
- ***Encryption***
- ***Decryption***
#### Usage
TODO-Instrucions

## SSH Automation
A tool for SSH Automation to upload/download a file or all files in a directory, bruteforce SSH password or username and password, bruteforce a password and also grab specific files given from a filelist.
- ***Upload files***
- ***Download files***
- ***Bruteforce passwords***
- ***Bruteforce usernames and passwords***
- ***Bruteforce and grab specified files***
#### Usage
TODO-Instructions

## Contribution
To contribute
1. Fork this repo
2. Create a new branch for your feature
3. Submit a pull request when done

All contributions are welcome!