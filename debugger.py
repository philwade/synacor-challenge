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

        self.func_map = {
            's' : 'step',
            'st': 'step_till',
            'r': 'run',
            'stack': 'stack',
            'reg': 'registers',
            'c': 'context',
            'set': 'set',
            'stack' : 'stack',
            'skset': 'skset',
            'sp': 'stackReplace',
        }

    def stackReplace(self, *new_values):
        new_stack = []
        for i in new_values:
            i = int(i)
            new_stack.append(i)
        self.vm.memory.stack = new_stack

    def stack(self):
        print self.vm.memory.stack

    def skset(self, index, value):
        index = int(index)
        value = int(value)
        self.vm.memory.stack.insert(index, value)

    def set(self, address, value):
        address = int(address)
        value = int(value)
        self.vm.memory.set(address, value)

    def registers(self):
        for i in range(32768, 32776):
            self.c.red_print("%i: %s" % (i, self.vm.memory.get(i)))

    def context(self, size):
        current_spot = self.vm.location
        size = int(size)

        for i in range(current_spot - 1, current_spot + size):
            address = self.vm.memory.getAddress(i)
            if address > 32767:
                val = "%s:%s" % (address, self.vm.memory.get(i))
            else:
                val = self.vm.memory.get(i)

            try:
                print "%i: %s, %i" % (i, self.codes[val], val)
            except KeyError:
                print "%i: %s" % (i, val)

    def run_cmd(self, cmd):
        parts = cmd.split(' ')
        f_name = self.func_map[parts[0]]
        func = getattr(self, f_name)

        func(*parts[1:])

    def go(self):
        while True:
            self.c.green_print('what do: ')
            cmd = raw_input()
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

    def run(self):
        runnin = True

        while runnin:
            try:
                self.vm.step(1)
            except KeyboardInterrupt:
                runnin = False
                self.vm.location -= 1

if __name__ == "__main__":
    v = Vm('challenge.bin')
    d = debugger(v)
    d.go()
