from vm import Vm

class color_printer:

    def __init__(self):
        self.green = '\033[0;32m'
        self.red = '\033[0;31m'
        self.ENDC = '\033[1;37m'

    def green_print(self, value):
        print self.green + value + self.ENDC

    def red_print(self, value):
        print self.red + value + self.ENDC

class debugger:
    def __init__(self, vm):
        self.vm = vm
        self.c = color_printer()

        self.func_map = {
            's' : 'step',
            'st': 'step_till',
        }

        self.codes = {
                0: 'EXIT',
                1: 'SET',
                2: 'PUSH',
                3: 'POP',
                4: 'EQ',
                5: 'GT',
                6: 'JMP',
                7: 'JT',
                8: 'JF',
                9: 'ADD',
                10: 'MULT',
                11: 'MOD',
                12: 'BAND',
                13: 'OR',
                14: 'NOT',
                15: 'RMEM',
                16: 'WMEM',
                17: 'CALL',
                18: 'RET',
                19: 'OUT',
                20: 'IN',
                21: 'NOOP',
        }

    def run_cmd(self, cmd):
        parts = cmd.split(' ')
        f_name = self.func_map[parts[0]]
        func = getattr(self, f_name)

        if parts[1]:
            func(parts[1])
        else:
            func()

    def go(self):
        while True:
            cmd = raw_input('what do: ')
            self.run_cmd(cmd)

    def step(self, n):
        n = int(n)
        self.vm.step(n)

    def step_till(self, op):
        current_op = ''

        while current_op != op:
            op_code = self.vm.memory.get(self.vm.location)
            current_op = self.codes[op_code]
            self.vm.step(1)

if __name__ == "__main__":
    v = Vm('challenge.bin')
    d = debugger(v)
    d.go()
