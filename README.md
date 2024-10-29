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
-We have the choice to scan a single ip-adress or multiple ip's given in a .txt file  
-Save the output of the scan to a file  
-Do a OS-Scan to see the most likely operating system  
-Use custom nmap flags (Altho the output will still be Hoststatus, Ports and services)  

A few examples:  
`python toolbox.py scanner 192.168.1.1 -s savefile.txt`  
`python toolbox.py scanner -m targets.txt -os`  
`python toolbox.py scanner -m targets.txt -s savefile.txt -c '-Pn -T4'`  
`python toolbox.py scanner 192.168.1.1 -c ' -T4`
I've noticed that when using the -c flag a space is needed after the first > ' < if only passing in one flag.  

Example output:
```
----------------------------------
Host: 255.255.255.0
State: up
Protocol: tcp
Port: 22, State: open, Service: SSH
```

### 2. *Using cryptotool*

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