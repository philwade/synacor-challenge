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
            self.registry[address % 8] = value

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
            6: self.jmp,
            7: self.jt,
            8: self.jf,
            9: self.add,
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
        target = self.memory.getAddress(self.location)
        self.location += 1
        a_value = self.memory.get(self.location)
        self.location += 1
        b_value = self.memory.get(self.location)
        value = (a_value + b_value) % 8
        self.memory.set(target, value)
        self.location += 1

    def eq(self):
        target = self.memory.getAddress(self.location)
        self.location += 1
        a_value = self.memory.get(self.location)
        self.location += 1
        b_value = self.memory.get(self.location)

        if a_value == b_value:
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
        self.location += 1
        target = self.memory.get(self.location)
        self.memory.set(target, value)
        self.location += 1

if __name__ == "__main__":
    v = Vm(sys.argv[1])
    v.run()
