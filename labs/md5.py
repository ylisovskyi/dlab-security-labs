from labs.list import *
import os


class MD5:

    Rs = [
        [7, 12, 17, 22],
        [5, 9, 14, 20],
        [4, 11, 16, 23],
        [6, 10, 15, 21]
    ]
    T = [
        [
            0xD76AA478, 0xE8C7B756, 0x242070DB, 0xC1BDCEEE,
            0xF57C0FAF, 0x4787C62A, 0xA8304613, 0xFD469501,
            0x698098D8, 0x8B44F7AF, 0xFFFF5BB1, 0x895CD7BE,
            0x6B901122, 0xFD987193, 0xA679438E, 0x49B40821
        ],
        [
            0xF61E2562, 0xC040B340, 0x265E5A51, 0xE9B6C7AA,
            0xD62F105D, 0x02441453, 0xD8A1E681, 0xE7D3FBC8,
            0x21E1CDE6, 0xC33707D6, 0xF4D50D87, 0x455A14ED,
            0xA9E3E905, 0xFCEFA3F8, 0x676F02D9, 0x8D2A4C8A
        ],
        [
            0xFFFA3942, 0x8771F681, 0x6D9D6122, 0xFDE5380C,
            0xA4BEEA44, 0x4BDECFA9, 0xF6BB4B60, 0xBEBFBC70,
            0x289B7EC6, 0xEAA127FA, 0xD4EF3085, 0x04881D05,
            0xD9D4D039, 0xE6DB99E5, 0x1FA27CF8, 0xC4AC5665
        ],
        [
            0xF4292244, 0x432AFF97, 0xAB9423A7, 0xFC93A039,
            0x655B59C3, 0x8F0CCC92, 0xFFEFF47D, 0x85845DD1,
            0x6FA87E4F, 0xFE2CE6E0, 0xA3014314, 0x4E0811A1,
            0xF7537E82, 0xBD3AF235, 0x2AD7D2BB, 0xEB86D391
        ]
    ]
    indices = [
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
        [1, 6, 11, 0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12],
        [5, 8, 11, 14, 1, 4, 7, 10, 13, 0, 3, 6, 9, 12, 15, 2],
        [0, 7, 14, 5, 12, 3, 10, 1, 8, 15, 6, 13, 4, 11, 2, 9]
    ]

    def __init__(self, arg=None):
        self.set_defaults()
        self.__list = LinkedList(None)
        if arg:
            self.__list.add(Node(arg, None))
            self.__hash(self.__list.to_string())
        self.length = 0
        self.digest_size = 16

    def set_defaults(self):
        self.__A = 0x67452301
        self.__B = 0xEFCDAB89
        self.__C = 0x98BADCFE
        self.__D = 0x10325476

        self.__list = LinkedList(None)

    def set(self, arg, file=False, file_size=None):
        self.set_defaults()
        self.__hash(arg, file, file_size)

    def update(self, arg, last_block=None):
        self.__hash(arg, last_block)

    def hexdigest(self):
        return ''.join(
            ["{:02x}".format(byte) for byte in bytearray(self.digest())]
        )

    def digest(self):
        res = b''
        buffers = [self.__A, self.__B, self.__C, self.__D]

        for buffer in buffers:
            bufferbytes = []
            b = bin(buffer).replace('b', '0')
            b = "0" * (34 - len(b)) + b

            bufferbytes.append(int(b[2:10], 2))
            bufferbytes.append(int(b[10:18], 2))
            bufferbytes.append(int(b[18:26], 2))
            bufferbytes.append(int(b[26:34], 2))

            res += bytes([bufferbytes[3]])
            res += bytes([bufferbytes[2]])
            res += bytes([bufferbytes[1]])
            res += bytes([bufferbytes[0]])

        return res

    def __hash(self, message, file=False, file_size=None):
        """Головна функція хешування MD5 """
        if file:
            chunks_count = (file_size // 64) + 1
            print(chunks_count)
            f, g, h, i, r = self.__f, self.__g, self.__h, self.__i, self.__r
            for chunk_index in range(chunks_count):
                print('{} out of {} chunks processed'.format(
                    chunk_index + 1, chunks_count
                ))
                chunk = message.read(64)
                chunk = self.__to_binary_string(chunk)
                if chunk_index == chunks_count - 1:
                    chunk = self.__pad(chunk, file_size)

                words = self.__create_word_array(chunk, file_size, chunk_index == chunks_count - 1)
                a, b, c, d = ca, cb, cc, cd = self.__A, self.__B, self.__C, self.__D
                funcs = [f, g, h, i]
                for j in range(4):
                    for k in range(4):
                        a = r(
                            funcs[j], a, b, c, d, words[self.indices[j][k * 4]],
                            self.Rs[j][0], self.T[j][k * 4]
                        )
                        d = r(
                            funcs[j], d, a, b, c,
                            words[self.indices[j][k * 4 + 1]],
                            self.Rs[j][1], self.T[j][k * 4 + 1]
                        )
                        c = r(
                            funcs[j], c, d, a, b,
                            words[self.indices[j][k * 4 + 2]],
                            self.Rs[j][2], self.T[j][k * 4 + 2]
                        )
                        b = r(
                            funcs[j], b, c, d, a,
                            words[self.indices[j][k * 4 + 3]],
                            self.Rs[j][3], self.T[j][k * 4 + 3]
                        )

                self.__A = (a + ca) & 0xffffffff
                self.__B = (b + cb) & 0xffffffff
                self.__C = (c + cc) & 0xffffffff
                self.__D = (d + cd) & 0xffffffff

            return
        if isinstance(message, bytes):
            length = len(message)
        else:
            length = len(message.encode('utf-8'))
        chunks = self.__split_to_blocks(
            self.__pad(self.__to_binary_string(message)), 512
        )
        f, g, h, i, r = self.__f, self.__g, self.__h, self.__i, self.__r

        for chunk in chunks:
            words = self.__create_word_array(
                chunk, length, chunks.index(chunk) == len(chunks) - 1
            )
            a, b, c, d = ca, cb, cc, cd = self.__A, self.__B, self.__C, self.__D

            funcs = [f, g, h, i]
            for j in range(4):
                for k in range(4):
                    a = r(
                        funcs[j], a, b, c, d, words[self.indices[j][k * 4]],
                        self.Rs[j][0], self.T[j][k * 4]
                    )
                    d = r(
                        funcs[j], d, a, b, c, words[self.indices[j][k * 4 + 1]],
                        self.Rs[j][1], self.T[j][k * 4 + 1]
                    )
                    c = r(
                        funcs[j], c, d, a, b, words[self.indices[j][k * 4 + 2]],
                        self.Rs[j][2], self.T[j][k * 4 + 2]
                    )
                    b = r(
                        funcs[j], b, c, d, a, words[self.indices[j][k * 4 + 3]],
                        self.Rs[j][3], self.T[j][k * 4 + 3]
                    )

            self.__A = (a + ca) & 0xffffffff
            self.__B = (b + cb) & 0xffffffff
            self.__C = (c + cc) & 0xffffffff
            self.__D = (d + cd) & 0xffffffff

    def __to_binary_string(self, string):
        """Створює двійкове представлення стрічки """
        if not isinstance(string, bytes):
            string = string.encode('utf-8')
        return ''.join(
            "{:08b}".format(byte) for byte in bytearray(string)
        )

    def __pad(self, bstring, length=None):
        """Додає доповнення до повідомлення """
        padded = ''
        length = length or len(bstring)

        bstring += "1"

        while (len(bstring) % 512) != 448:
            bstring += "0"

        padded += bstring + self.__pad64b(length)

        return padded

    def __pad64b(self, length):
        """Створює 64-бітне представлення довжини повідомлення """
        s = bin(length).replace('b', '0')

        # Для уникнення переповнення
        if len(s) > 64:
            return '0' + '1' * 63

        padded = "0" * (64 - len(s)) or ''
        padded += s[::-1]  # збереження правильного порядку
        return padded[::-1]

    def __split_to_blocks(self, message, n):
        """Допоміжний метод для поділу стрічки на рівні блоки """
        return [message[i:i + n] for i in range(0, len(message), n)]

    def __create_word_array(self, message, message_length, final_block):
        """Ділить повідомлення на слова довжиною по 16 біт """
        message = self.__split_to_blocks(message, 32)
        word_array = [0] * 16

        word_index = 0
        for word in message:
            _bytes = self.__split_to_blocks(word, 8)
            powers = 0

            for byte in _bytes:
                temp_byte = word_array[word_index]
                temp_byte = temp_byte | int(byte, 2) << powers
                powers += 8
                word_array[word_index] = temp_byte

            word_index += 1

        # виправлення останніх двох байтів якщо це останній блок
        if final_block:
            word_array[-2] = message_length << 3
            word_array[-1] = message_length >> 29

        return word_array

    def __f(self, x, y, z):
        """Функція F """
        return (x & y) | ((~x) & z)

    def __g(self, x, y, z):
        """Функція G """
        return (x & z) | (y & (~z))

    def __h(self, x, y, z):
        """Функція H """
        return x ^ y ^ z

    def __i(self, x, y, z):
        """Функція I """
        return y ^ (x | (~z))

    def __rotate_left(self, x, n):
        """Rotates x left by n (note that Python bitshift is arithmetic) """
        return (x << n) | (x >> (32 - n))

    def __r(self, function, a, b, c, d, x, s, ac):
        """Функція для обробки повідомлення в кожному раунді """
        r = a + function(b, c, d)
        r = r + x
        r = r + ac
        r = r & 0xffffffff
        r = self.__rotate_left(r, s)
        r = r & 0xffffffff
        r = r + b

        return r & 0xffffffff  # Робимо r позитивним
