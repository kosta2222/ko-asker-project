from ._command import Command
import traceback


class Stop(Command):
    def execute(self, args=[]):
        print('by-by)')
        return "stop"

    def __repr__(self):
        return 'stops the shell'


class Input(Command):
    def __init__(self):
        pass

    def execute(self, args):
        return input('new->').strip()

    def __repr__(self):
        return 'New input string to stack'


class InputNargs(Command):
    def __init__(self):
        pass

    def execute(self, args):
        return int(input('nargs->').strip())

    def __repr__(self):
        return 'number of args to take from stack'


class Shell:
    def __init__(self,):
        self._cmd = {'s': Stop(), 'i': Input(),
                      'n': InputNargs()}
        self.stack = []

    def set_cmd(self, cmd):
        self._cmd.update(cmd)

    def loop(self):
        shell_running = True
        res = None
        nargs = 0
        # print possibilities
        for key in self._cmd.keys():
            print(key, ':', self._cmd.get(key), end='| ')
        print()
        while shell_running:
          try:  
            s = input('->')
            s = s.strip()
            obj = self._cmd.get(s)
            len_stack = len(self.stack)
            if obj is not None:
                if  nargs == 0:
                    res = obj.execute(args=[])
                else:
                    args = []
                    back_index = len_stack 
                    forward_index = len_stack - nargs
                    # pass parameters from stack
                    for i in range(forward_index, back_index):
                        args.append(self.stack[i])
                    res = obj.execute(args)
                    self.stack.clear() 
                    nargs=0   

                if isinstance(res, int) and res == 0:
                    continue
                elif isinstance(res, str) and res =='stop':
                    break

                elif isinstance(res, str):
                    self.stack.append(res)
                elif isinstance(res, int) and res > 0:
                    nargs = res

                print('stack', self.stack)    

            else:
                print('Unrecognized op')
          except Exception as e:
             traceback.print_tb(e.__traceback__)
             traceback.print_exc()    
