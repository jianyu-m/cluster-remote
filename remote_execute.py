#!/bin/python

import sys
from remote_process import RemoteProcess
import config as config
import subprocess
import os

def execute(command, servers=config.servers, is_shared=True, context_pre = "", will_wait=True, user=config.user, is_sudo=False, sudo_passwd=config.passwd): 
    remotes = []
    for server in servers:
        remote = RemoteProcess(server, user, context_pre, command, is_shared, is_sudo, sudo_passwd)
        remote.start()
        remotes.append(remote)

    if will_wait:
        for remote in remotes:
            remote.wait()

def unique_execute(command, servers=config.servers, is_shared=True, context_pre="", will_wait=True, user=config.user, is_sudo=False, sudo_passwd=config.passwd):
    us = set(servers)
    execute(command, us, is_shared, will_wait, context_pre, user, is_sudo, sudo_passwd)

def local_execute(command, will_wait=True):
    os.system(command)

class connect:
    """Context manager for changing the current working directory"""
    def __init__(self, host, context, is_shared,user=config.user, is_sudo=False, sudo_passwd=config.passwd):
        self.remote = RemoteProcess(host, user, context, "", is_shared, is_sudo, sudo_passwd)

    def __enter__(self):
        return self

    def __exit__(self, etype, value, traceback):
        pass

    def execute(self, command, is_sudo=False):
        self.remote.execute(command, is_sudo)

    def get(self, f, t):
        self.remote.get(f, t)

    def put(self, f, t):
        self.remote.put(f, t)

def run_once(func):
    def wrapper():
        filename = "%s.once" % func.__name__
        if os.path.exists(filename):
            print "%s has been executed" % func.__name__
            return
        func()
        open(filename, 'w').close()
        
    return wrapper

# unique_execute(sys.argv[1], is_shared=False)

