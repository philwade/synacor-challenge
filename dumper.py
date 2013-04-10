from vm import *
from debugger import debugger
v = Vm('challenge.bin')
d = debugger(v)

m = v.memory.memory
for i in range(0, len(m)):
    try:
        print "%i: %s, %i" % (i, d.codes[m[i]], m[i])
    except KeyError:
        print "%i: %s" % (i, m[i])
