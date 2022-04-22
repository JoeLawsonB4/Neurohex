#----------------------------------------------------------------------------
# Opens connection to GTP program. 
#----------------------------------------------------------------------------

from __future__ import absolute_import
from __future__ import print_function
import string, os, sys, subprocess, signal
from subprocess import Popen, PIPE

#----------------------------------------------------------------------------

class Program:
    class CommandDenied(Exception):
        pass

    class Died(Exception):
        pass

    def __init__(self, command, verbose):
        self._command = command
        self._verbose = verbose
        
        if self._verbose:
            print(("Creating program: "+command))
        #self._stdin, self._stdout, self._stderr = subprocess.os.popen3(command)
        print(command)
        p = Popen(['py',command], shell = True, stdin=PIPE, stdout=PIPE, 
            stderr=PIPE, close_fds=True, universal_newlines=True)
        poll = p.poll()
        if poll is None:
            print("alive")
        self.p = p
        self._pid = p.pid
        self._stdin, self._stdout, self._stderr = (p.stdin, p.stdout, p.stderr)
        self._isDead = 0

    def getCommand(self):
        return self._command

    def getDenyReason(self):
        return self._denyReason

    def getName(self):
        name = "?"
        try:
            name = self.sendCommand("name").strip()
            version = self.sendCommand("version").strip()
            name += " " + version
        except Program.CommandDenied:
            pass
        return name

    def isDead(self):
        return self._isDead

    def sendCommand(self, cmd):
        try:
            if self._verbose:
                print(("< " + cmd))
            self._stdin.write(cmd + "\r\n")
            self._stdin.flush()
            return self._getAnswer()
        except IOError:
            poll = self.p.poll()
            if poll is None:
                print("alive")
            self._programDied()

    def _getAnswer(self):
        answer = ""
        done = 0
        numberLines = 0
        first = True
        while not done:
            lines = self._stdout.readlines()
            line = self._stdout.readline()
            print(lines)
            if line == "":
                self._programDied()
            if self._verbose:
                sys.stdout.write("> " + line)
            if first:
                if not (line[0]=="=" or line[0]=="?"):
                    continue
                else:
                    first = False
            numberLines += 1
            done = (line == "\r\n")
            if not done:
                answer += line
        if answer[0] != '=':
            self._denyReason = answer[2:].strip()
            raise Program.CommandDenied
        if numberLines == 1:
            return answer[1:].strip()
        return answer[2:]

    def _programDied(self):
        self._isDead = 1
        raise Program.Died

    def terminate(self):
        try:
            os.killpg(os.getpgid(self._pid), signal.SIGTERM)
        except OSError:
            pass

