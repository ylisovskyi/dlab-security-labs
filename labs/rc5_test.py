

class RC5(object):

    def __init__(self, w, R, b, key):
        self.w = w
        self.R = R
        self.key = key
        self.T = 2 * (R + 1)
        self.w4 = w // 4
        self.w8 = w // 8
        self.mod = 2 ** self.w
        self.mask = self.mod - 1
        self.b = b
        self.c = self.b // self.w8
        self.__keyAlign()
        self.__keyExtend()
        self.__shuffle()

    def __lshift(self, val, r_bits, max_bits):
        v1 = (val << r_bits % max_bits) & (2 ** max_bits - 1)
        v2 = ((val & (2 ** max_bits - 1)) >> (max_bits - (r_bits % max_bits)))
        return v1 | v2

    def __rshift(self, val, r_bits, max_bits):
        v1 = ((val & (2 ** max_bits - 1)) >> r_bits % max_bits)
        v2 = (val << (max_bits - (r_bits % max_bits)) & (2 ** max_bits - 1))

        return v1 | v2

    def __keyAlign(self):
        if len(self.key) % self.w8:
            self.key += b'\x00' * (self.w8 - len(self.key) % self.w8)
        L = []
        for i in range(len(self.key) // self.c):
            L.append(self.key[i * self.c:i * self.c + self.c])
        self.L = L
        print(self.L)

    def __const(self):
        if self.w == 16:
            return 0xB7E1, 0x9E37
        elif self.w == 32:
            return 0xB7E15163, 0x9E3779B9
        elif self.w == 64:
            return 0xB7E151628AED2A6B, 0x9E3779B97F4A7C15

    def __keyExtend(self):
        P, Q = self.__const()
        self.S = [P] * self.T
        for i in range(1, self.T):
            self.S[i] = self.S[i - 1] + Q

    def __shuffle(self):
        i, j, A, B = 0, 0, 0, 0
        for k in range(3 * max(self.c, self.T)):
            A = self.S[i] = (self.S[i] + A + B) << 3
            l = int.from_bytes(self.L[j], byteorder='little')
            B = self.L[j] = (l + A + B) << (A + B)
            i = (i + 1) % self.T
            j = (j + 1) % self.c

    def encryptBlock(self, data):
        A = int.from_bytes(data[:self.w8], byteorder='little')
        B = int.from_bytes(data[self.w8:], byteorder='little')
        A = (A + self.S[0]) % self.mod
        B = (B + self.S[1]) % self.mod
        for i in range(1, self.R + 1):
            A = (((A ^ B) << B) + self.S[2 * i]) % self.mod
            B = (((A ^ B) << A) + self.S[2 * i + 1]) % self.mod
        return A.to_bytes(self.w8, byteorder='little')

    def encryptFile(self, inpFileName, outFileName):
        with open(inpFileName, 'rb') as inp, open(outFileName, 'wb') as out:
            run = True
            while run:
                text = inp.read(self.w4)
                if not text:
                    break
                if len(text) != self.w4:
                    text = text.ljust(self.w4, b'\x00')
                    run = False
                text = self.encryptBlock(text)
                out.write(text)

    def decryptBlock(self, data):
        A = int.from_bytes(data[:self.w8], byteorder='little')
        B = int.from_bytes(data[self.w8:], byteorder='little')
        for i in range(self.R, 0, -1):
            B = (B - self.S[2 * i + 1] >> A) ^ A
            A = (A - self.S[2 * i] >> B) ^ B
        B = (B - self.S[1]) % self.mod
        A = (A - self.S[0]) % self.mod
        return (A.to_bytes(self.w8, byteorder='little')
                + B.to_bytes(self.w8, byteorder='little'))

    def decryptFile(self, inpFileName, outFileName):
        with open(inpFileName, 'rb') as inp, open(outFileName, 'wb') as out:
            run = True
            while run:
                text = inp.read(self.w4)
                if not text:
                    break
                if len(text) != self.w4:
                    run = False
                text = self.decryptBlock(text)
                if not run:
                    text = text.rstrip(b'\x00')
                out.write(text)
