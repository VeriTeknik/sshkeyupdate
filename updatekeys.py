#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Update SSH Keys in Remote Servers"""

# M. Emre Aydin - http://about.me/emre.aydin

import paramiko
import socket
import sys
import ConfigParser


def is_ssh_port(hostname, port, timeout):
    """Check if 22 is an SSH port on host"""
    try:
        socket.setdefaulttimeout(timeout)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((hostname, port))
        s.sendall("a")
        s.shutdown(socket.SHUT_WR)
        data = s.recv(1024)
        if "SSH" in data:
            return True
        else:
            return False
    except Exception as err:
        print("Exception occurred: {0}".format(str(err)))
        return False


def insert_key(newKey, filename, ssh):
    """insert key to file"""
    ssh.exec_command("grep -q -F '%s' %s || echo %s >> %s" % (newKey, filename, newKey, filename))


def replace_key(newKey, oldKey, filename, ssh):
    """replace key at file, obselete"""
    ssh.exec_command("sed -i 's;%s;%s;g' %s" % (oldKey, newKey, filename))


def delete_key(oldKey, filename, ssh):
    """delete key from file"""
    ssh.exec_command("sed -i '/%s/d' %s" % (oldKey, filename))


def check_ssh_file(filename, ssh):
    """check if ssh file exists"""
    stdin, stdout, stderr = ssh.exec_command("[ ! -f %s ] && echo \"0\"" % filename)
    output = stdout.readlines()
    if len(output) == 0:
        return True
    else:
        return False


def create_ip_range(start_ip, end_ip):
    """create range of ip addresses"""
    start = list(map(int, start_ip.split(".")))
    end = list(map(int, end_ip.split(".")))
    temp = start
    ip_range = []

    ip_range.append(start_ip)
    while temp != end:
        start[3] += 1
        for i in (3, 2, 1):
            if temp[i] == 256:
                temp[i] = 0
                temp[i - 1] += 1
        ip_range.append(".".join(map(str, temp)))

    return ip_range


if __name__ == "__main__":

    # Check Argument Length
    if len(sys.argv) < 3:
        print("Enter the IP Range.")
        raise SystemExit

    first_ip = sys.argv[1]
    second_ip = sys.argv[2]

    # Generate IP Ranges
    try:
        iprange = create_ip_range(first_ip, second_ip)
    except Exception as err:
        print("Probable IP Range Definition Error: {0}".format(str(err)))
        raise SystemExit

    for i in iprange:
        print i
    while True:
        answer = raw_input("These are the hosts to connect. Continue?\n(yes/no)")
        if answer == "yes":
            break
        if answer == "no":
            raise SystemExit

    # Check the settings in config file
    try:
        config = ConfigParser.ConfigParser()
        config.read('config')
    except Exception as err:
        print("Config read failed: {0}".format(str(err)))
        raise SystemExit

    try:
        user = config.get('connect', 'user')
        keyfile = config.get('connect', 'keyfile')
        keypass = config.get('connect', 'keypass')
        authfile = config.get('connect', 'authfile')
        authfile2 = config.get('connect', 'authfile2')
        timeout = config.getint('connect', 'timeout')
        port = config.getint('connect', 'port')
    except Exception as err:
        print("Error Parsing the config file: {0}".format(str(err)))
        raise SystemExit

    # Get Keys to INSERT, if any
    INSERT_keys = []
    if config.has_section('insert') and len(config.options('insert')) > 0:
        INSERT_MODE = True
        for i in config.options('insert'):
            INSERT_keys.append(config.get('insert', i))
    else:
        INSERT_MODE = False

    # Get Keys to DELETE, if any
    DELETE_keys = []
    if config.has_section('delete') and len(config.options('delete')) > 0:
        DELETE_MODE = True
        for i in config.options('delete'):
            DELETE_keys.append(config.get('delete', i))
    else:
        DELETE_MODE = False

    # log = open("keys_log", "a")

    # Create SSH Connection Instance and Private Key File Instance
    key = paramiko.RSAKey.from_private_key_file(keyfile, password=keypass)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    not_found = []
    for ip in iprange:
        s_con_stat = 0
        if is_ssh_port(ip, port, 1):
            try:
                ssh.connect(hostname=ip, port=port, username=user, pkey=key, timeout=timeout)
                s_con_stat = 1
            except Exception as err:
                print("Error while connecting to : {0}".format(ip))
                print("Error: {0}".format(str(err)))
                s_con_stat = 0
            if s_con_stat:
                if check_ssh_file(authfile, ssh):
                    if INSERT_MODE:
                        for i in INSERT_keys:
                            insert_key(i, authfile, ssh)
                            print("Key {0} inserted to file {1} at {2}".format(i, authfile, ip))
                    if DELETE_MODE:
                        for i in DELETE_keys:
                            delete_key(i, authfile, ssh)
                            print("Key {0} deleted from file {1} at {2}".format(i, authfile, ip))

                elif check_ssh_file(authfile2, ssh):
                    if INSERT_MODE:
                        for i in INSERT_keys:
                            insert_key(i, authfile2, ssh)
                            print("Key {0} inserted to file {1} at {2}".format(i, authfile2, ip))
                    if DELETE_MODE:
                        for i in DELETE_keys:
                            delete_key(i, authfile2, ssh)
                            print("Key {0} deleted from file {1} at {2}".format(i, authfile2, ip))
        else:
            print("SSH Port Not Found at : {0}".format(ip))
            not_found.append(ip)

    print("End of Script")
    if len(not_found) > 0:
        print("Unable to connect to following Hosts:")
        for i in not_found:
            print i
