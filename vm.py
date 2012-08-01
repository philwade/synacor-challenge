import sys
import inspect
from array import array

class Memory:
    def __init__(self, filehandle):
        self.memory = array('H')
        self.registry = array('H', [0 for i in range(8)])
        self.stack = []

        filestring = filehandle.read()
        self.memory.fromstring(filestring)

    def get(self, address):
        if address < 32768:
            value = self.memory[address]
            if value >= 32768:
                return self.registry[value % 8]
            return value
        else:
            return self.registry[address % 8]

    def set(self, address, value):
        if address < 32768:
            self.memory[address] = value
        else:
            self.registry[address % 8] = value % 32768

    # for when we don't want transparent registry access
    def getAddress(self, address):
        return self.memory[address]

    def push(self, value):
        self.stack.append(value) # lists behave opposite normal stacks, so we work in reverse

    def pop(self):
        return self.stack.pop()

class Vm:
    def __init__(self, filename):
        f = open(filename)
        self.memory = Memory(f)
        self.location = 0

        self.ops = {
            0: exit,
            1: self.set,
            2: self.push,
            3: self.pop,
            4: self.eq,
            5: self.gt,
            6: self.jmp,
            7: self.jt,
            8: self.jf,
            9: self.add,
            10: self.mult,
            11: self.mod,
            12: self.band,
            13: self.bor,
            14: self.bnot,
            15: self.rmem,
            16: self.wmem,
            17: self.call,
            18: self.ret,
            19: self.out,
            21: self.noop,
        };

    def run(self):
        while True:
            instruction = self.memory.get(self.location)
            if instruction in self.ops:
                func = self.ops[instruction]
                self.location += 1 #we always want the next value going into an op
                func()
            else:
                print "unknown opcode: %i" % instruction
                exit()

    def noop(self):
        print "noop!"

    def out(self):
        charcode = self.memory.get(self.location)
        sys.stdout.write(chr(charcode))
        self.location += 1

    def jmp(self):
        newlocation = self.memory.get(self.location)
        self.location = newlocation

    def jt(self):
        a_value = self.memory.get(self.location)
        self.location += 1
        if a_value != 0:
            b_value = self.memory.get(self.location)
            self.location = b_value
        else:
            self.location += 1

    def jf(self):
        a_value = self.memory.get(self.location)
        self.location += 1
        if a_value == 0:
            b_value = self.memory.get(self.location)
            self.location = b_value
        else:
            self.location += 1

    def set(self):
        target = self.memory.getAddress(self.location)
        self.location += 1
        value = self.memory.get(self.location)
        self.memory.set(target, value)
        self.location += 1

    def add(self):
        target, a, b = self._addressAndTwoValues()
        self.memory.set(target, a + b)
        self.location += 1

    def eq(self):
        target, a, b = self._addressAndTwoValues()

        if a == b:
            self.memory.set(target, 1)
        else:
            self.memory.set(target, 0)
        self.location += 1

    def push(self):
        value = self.memory.get(self.location)
        self.memory.push(value)
        self.location += 1

    def pop(self):
        value = self.memory.pop()
        target = self.memory.getAddress(self.location)
        self.memory.set(target, value)
        self.location += 1

    def gt(self):
        target, b, c = self._addressAndTwoValues()

        if b > c:
            self.memory.set(target, 1)
        else:
            self.memory.set(target, 0)
        self.location += 1

    def band(self):
        target, b, c = self._addressAndTwoValues()
        self.memory.set(target, b & c)
        self.location += 1

    def bor(self):
        target, a, b = self._addressAndTwoValues()
        self.memory.set(target, a | b)
        self.location += 1

    def bnot(self):
        target = self.memory.getAddress(self.location)
        self.location += 1
        value = self.memory.get(self.location)
        self.memory.set(target, ~value)
        self.location += 1

    def call(self):
        next_instruction_address = self.location + 1
        self.memory.push(next_instruction_address)
        jump_to = self.memory.get(self.location)
        self.location = jump_to

    def mult(self):
        target, a, b = self._addressAndTwoValues()
        self.memory.set(target, a * b)
        self.location += 1

    def mod(self):
        target, a, b = self._addressAndTwoValues()
        self.memory.set(target, a % b)
        self.location += 1

    def rmem(self):
        target = self.memory.getAddress(self.location)
        self.location += 1
        value_to_get = self.memory.get(self.location)
        value = self.memory.get(value_to_get)
        self.memory.set(target, value)
        self.location += 1

    def wmem(self):
        target = self.memory.get(self.location)
        self.location += 1
        value = self.memory.get(self.location)
        self.memory.set(target, value)
        self.location += 1

    def ret(self):
        jump_to = self.memory.pop()
        self.location = jump_to

    def _addressAndTwoValues(self):
        target = self.memory.getAddress(self.location)
        self.location += 1
        a_value = self.memory.get(self.location)
        self.location += 1
        b_value = self.memory.get(self.location)

        return target, a_value, b_value

if __name__ == "__main__":
    v = Vm(sys.argv[1])
    v.run()
