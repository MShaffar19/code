INS = ['moo', 'mOo', 'moO', 'mOO', 'Moo', 'MOo',
       'MoO', 'MOO', 'OOO', 'MMM', 'OOM', 'oom']

HLP = dict((s, i) for i, s in enumerate(INS))

import sys
import msvcrt

################################################################################

class COD:

    def __init__(self, code):
        for ins in code:
            assert 0 <= ins < len(INS)
        self.cod = code
        self.pos = 0

    def get(self):
        return self.cod[self.pos]

    def inc(self):
        self.pos += 1
        if self.pos == len(self.cod):
            raise SystemExit

    def dec(self):
        self.pos -= 1
        assert self.pos >= 0

################################################################################

class MEM:
    
    def __init__(self):
        self.mem = {}
        self.pos = 0
        
    def get(self):
        if self.pos in self.mem:
            return self.mem[self.pos]
        return 0
    
    def set(self, value):
        if value:
            self.mem[self.pos] = value
        elif self.pos in self.mem:
            del self.mem[self.pos]

    def inc(self):
        self.pos += 1

    def dec (self):
        self.pos -= 1

################################################################################

def parse(string):
    index = 0
    code = []
    ins = string[index:index+3]
    while len(ins) == 3:
        if ins in INS:
            code.append(INS.index(ins))
            index += 3
        else:
            index += 1
        ins = string[index:index+3]
    return tuple(code)

DECODE = ['END', 'P--', 'P++', 'EXE', 'I/O', 'M--',
          'M++', 'LOP', 'M=0', 'REG', 'OUT', 'INP']

def decode(code):
    for ins in code:
        print INS[ins] + '\t' + DECODE[ins]
    print

def engine(code):
    global REG
    REG = None
    mem = MEM()
    cod = COD(code)
    ins = cod.get()
    while True:
        ins = run(mem, cod, ins)

def run(mem, cod, ins):
    global REG
    # INS - 0 - moo
    if ins == 0:
        cod.dec()
        cod.dec()
        # INIT
        level = 1
        temp = cod.get()
        if temp == HLP['moo']:
            level += 1
        elif temp == HLP['MOO']:
            level -= 1
        while level:
            # LOOP
            cod.dec()
            temp = cod.get()
            if temp == HLP['moo']:
                level += 1
            elif temp == HLP['MOO']:
                level -= 1
        return HLP['MOO']
    # INS - 1 - mOo
    elif ins == 1:
        mem.dec()
        cod.inc()
        return cod.get()
    # INS - 2 - moO
    elif ins == 2:
        mem.inc()
        cod.inc()
        return cod.get()
    # INS - 3 - mOO
    elif ins == 3:
        temp = mem.get()
        assert temp != 3
        if 0 <= temp < len(INS):
            return run(mem, cod, temp)
        else:
            raise SystemExit
    # INS - 4 - Moo
    elif ins == 4:
        temp = mem.get()
        if temp:
            sys.stdout.write(chr(temp & 0x7F))
        else:
            char = get_char()
            mem.set(ord(char) & 0x7F)
        cod.inc()
        return cod.get()
    # INS - 5 - MOo
    elif ins == 5:
        mem.set(mem.get() - 1)
        cod.inc()
        return cod.get()
    # INS - 6 - MoO
    elif ins == 6:
        mem.set(mem.get() + 1)
        cod.inc()
        return cod.get()
    # INS - 7 - MOO
    elif ins == 7:
        temp = mem.get()
        if temp:
            cod.inc()
            return cod.get()
        else:
            cod.inc()
            cod.inc()
            # INIT
            level = 1
            temp = cod.get()
            if temp == HLP['moo']:
                level -= 1
            elif temp == HLP['MOO']:
                level += 1
            while level:
                # LOOP
                cod.inc()
                temp = cod.get()
                if temp == HLP['moo']:
                    level -= 1
                elif temp == HLP['MOO']:
                    level += 1
            cod.inc()
            return cod.get()
    # INS - 8 - OOO
    elif ins == 8:
        mem.set(0)
        cod.inc()
        return cod.get()
    # INS - 9 - MMM
    elif ins == 9:
        if REG is None:
            REG = mem.get()
        else:
            mem.set(REG)
            REG = None
        cod.inc()
        return cod.get()
    # INS - 10 - OOM
    elif ins == 10:
        sys.stdout.write(str(mem.get()) + '\n')
        cod.inc()
        return cod.get()
    # INS - 11 - oom
    elif ins == 11:
        mem.set(get_int())
        cod.inc()
        return cod.get()
    # ERROR
    else:
        raise Exception

def get_char():
    while msvcrt.kbhit():
        msvcrt.getch()
    func = False
    char = msvcrt.getch()
    if char in ('\x00', '\xE0'):
        func = True
    while func:
        msvcrt.getch()
        func = False
        char = msvcrt.getch()
        if char in ('\x00', '\xE0'):
            func = True
    return char.replace('\r', '\n')

def get_int():
    while msvcrt.kbhit():
        msvcrt.getch()
    buff = ''
    char = msvcrt.getch()
    while char != '\r' or not buff:
        if '0' <= char <= '9':
            sys.stdout.write(char)
            buff += char
        char = msvcrt.getch()
    sys.stdout.write('\n')
    return int(buff)

################################################################################

def main():
    path = raw_input('Run File: ') + '.cow'
    code = parse(file(path).read())
    decode(code)
    engine(code)
        
################################################################################

if __name__ == '__main__':
    INS, DECODE = DECODE, INS
    try:
        main()
    except SystemExit:
        raw_input()
    except:
        import traceback
        raw_input(traceback.format_exc())
