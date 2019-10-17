from tkinter import *


LAB_2_TEST_SET = {
    '': 'D41D8CD98F00B204E9800998ECF8427E',
    'a': '0CC175B9C0F1B6A831C399E269772661',
    'abc': '900150983CD24FB0D6963F7D28E17F72',
    'message digest': 'F96B697D7CB7938D525A2F31AAF161D0',
    'abcdefghijklmnopqrstuvwxyz': 'C3FCD3D76192E4007DFB496CCA67E13B',
    'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789': (
        'D174AB98D277D9F5A5611C2C9F419D9F'
    ),
    (
        '1234567890123456789012345678901234567890'
        '1234567890123456789012345678901234567890'
    ): '57EDF4A22BE3C955AC49DA2E2107B67A'
}
LAB_1_LABELS = {
    'Згенерована послідовність:': (270, 0),
    'Модуль порівняння (m)': (0, 0),
        'Базис:': (20, 1),
        'Степінь:': (20, 2),
        'Додаток:': (20, 3),
    'Множник (a):': (0, 4),
        'Базис: ': (20, 5),
        'Степінь: ': (20, 6),
    'Приріст (c):': (0, 7),
    'Початкове значення (Xo):': (0, 8),
    'Кількість чисел для виводу:': (0, 10),
    'Період функції:': (270, 14),
}
LAB_1_SPINS = {
    (0, 10, 2): 1,
    (1, 32, 18): 2,
    (-20, 20, -1): 3,
    (1, 20, 5): 5,
    (1, 20, 3): 6,
    (0, 10 ** 4, 34): 7,
    (1, 1024, 512): 8,
    (0, 2 ** 31, 1): 10
}
LAB_2_LABELS = {
    'Згенерований MD5-хеш:': (0, 7.5),
    'Завантажений MD5-хеш': (0, 10.5),
    'Ваша стрічка': (0, 0),
    'Коректність:': (10, 14),
    '': (80, 14)
}
WIDTH = 500
HEIGHT = 400
MULTIPLIER = 25


def create_window(name):
    window = Tk()
    window.title(name)
    window.geometry('{}x{}'.format(WIDTH, HEIGHT))
    return window


def place_labels(window, labels_info):
    labels = []
    for text, coords in labels_info.items():
        label = Label(window, text=text)
        label.place(x=coords[0], y=coords[1] * MULTIPLIER)
        labels.append(label)

    return labels


def place_spins(window, spins_info):
    spins = []
    for vals, y_coord in spins_info.items():
        spin = Spinbox(
            window,
            from_=vals[0],
            to=vals[1],
            width=12,
            textvariable=IntVar(value=vals[2])
        )
        spin.place(x=180, y=y_coord * MULTIPLIER)
        spins.append(spin)

    return spins
