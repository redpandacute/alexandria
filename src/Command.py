class Command:

    def __init__(self, cmdstr):
        self.cmdstr = cmdstr
        self.args = cmdstr.split(' ')
        self.cmd = self.args[0]

    def getCmd(self):
        return self.cmd
