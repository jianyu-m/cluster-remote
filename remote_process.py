
import subprocess
import os

class RemoteProcess:
    def __init__(self, host, user, idx, command, share, is_sudo, sudo_passwd):
        self.host = host
        self.command = command
        self.user = user
        self.remote = None
        self.idx = idx
        self.share = share
        self.host_idx = "%s-%s" % (self.host, self.idx)
        if self.share == False:  
            self.new_context = "mkdir -p %s; cd %s;" % (self.host_idx, self.host_idx)
        else:
            self.new_context = ""
        if is_sudo == True:
            self.sudo = "echo %s | sudo -S " % sudo_passwd
        else:
            self.sudo = ""

    def start(self):
        self.remote = subprocess.Popen(["ssh", "%s@%s" % (self.user, self.host), "%s%s%s" % (self.sudo, self.new_context, self.command)])
        print("execute binary on %s with %s" % (self.host, self.command))

    def execute(self, command, is_sudo=False, will_wait=True):
        remote = subprocess.Popen(["ssh", "%s@%s" % (self.user, self.host), "%s%s%s" % (self.sudo, self.new_context, command)])
        if will_wait:
            remote.wait()
        print("execute binary on %s with %s" % (self.host, command))
        return remote

    def get(self, filename, cur):
        remote = subprocess.Popen(["scp", "%s@%s:~/%s/%s" % (self.user, self.host, self.host_idx, filename), cur])
        remote.wait()

    def put(self, cur, filename):
        remote = subprocess.Popen(["scp", cur, "%s@%s:~/%s/%s" % (self.user, self.host, self.host_idx, filename)])
        remote.wait()

    def kill(self):
        self.remote.kill()
        print("stop host %s" % self.host)

    def wait(self):
        self.remote.wait()