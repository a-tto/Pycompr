WOPEN = 'wb'
ROPEN = 'rb'

def getc(f):
    c = f.read(1)
    if c == '':
        return None
    return ord(c)

def putc(f, x):
    f.write(chr(x & 0xff))

class BitIO():
    def __init__(self, name, mode):
        if mode == ROPEN:
            self.cnt = 0
        elif mode == WOPEN:
            self.cnt = 8
        else:
            raise 'BitIO: file mode error'

        self.mode = mode
        self.file = open(name,mode)
        self.buf = 0

    def close(self):
        if self.mode == WOPEN and self.cnt < 8:
            putc(self.file,self.buf)
        self.file.close()

    def getbit(self):
        self.cnt -= 1
        if self.cnt < 0:
            self.buf = getc(self.file)
            if self.buf is None:
                return None
            self.cnt = 7
        return (self.buf >> self.cnt) & 1
    
    def putbit(self, bit):
        self.cnt -= 1
        if bit == 1:
            self.buf |= (1 << self.cnt)
        if self.cnt == 0:
            putc(self.file, self.buf)
            self.buf = 0
            self.cnt = 8

    def getbits(self, n):
        v = 0
        p = 1 << (n-1)
        while p > 0:
            if self.getbit() == 1:
                v |= p
                p >>= 1
        return v
    
    def putbits(self, x, n):
        p = 1 << (n-1)
        while p > 0:
            self.putbit(x & p)
            p >>= 1
