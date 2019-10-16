from tkinter import *
from tkinter import scrolledtext


def set_values():
    global a, m, c, rand, spins
    m = int(spins[0].get()) ** int(spins[1].get()) + int(spins[2].get())
    a = int(spins[3].get()) ** int(spins[4].get())
    c = int(spins[5].get())
    rand = int(spins[6].get())


def write_to_file():
    set_values()
    with open('out-lab-1.txt', 'w') as fp:
        prev = None
        first = rand
        fp.write(str(rand) + '\n')
        i = 0
        while i < m:
            num = lcg()
            fp.write(str(num) + '\n')
            if (prev and num == prev) or num == first:
                break
            prev = num
            i += 1


def generate():
    set_values()
    prev = None
    first = rand
    txt.delete(0.0, END)
    count = int(spins[7].get())
    txt.insert(END, rand)
    txt.insert(END, '\n')
    for i in range(count):
        num = lcg()
        txt.insert(END, num)
        txt.insert(END, '\n')
        if (prev and num == prev) or num == first:
            period_label.config(text=str(i + 1))
            break
        prev = num
    write_to_file()


def lcg():
    global rand
    rand = (a * rand + c) % m
    return rand


window = Tk()

WIDTH = 500
HEIGHT = 400

multiplier = 25

m = 2 ** 18 - 1
a = 5 ** 3
c = 34
rand = 512

window.title('Lab 1')
window.geometry('{}x{}'.format(WIDTH, HEIGHT))
labels_info = {
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
spins_info = {
    (0, 10, 2): 1,
    (1, 32, 18): 2,
    (-20, 20, -1): 3,
    (1, 20, 5): 5,
    (1, 20, 3): 6,
    (0, 10 ** 4, 34): 7,
    (1, 1024, 512): 8,
    (0, m, 1): 10
}
spins = []
period_label = Label(window, text='')
period_label.place(x=360, y=14 * multiplier)
for text, coords in labels_info.items():
    label = Label(window, text=text)
    label.place(x=coords[0], y=coords[1] * multiplier)

for vals, y_coord in spins_info.items():
    var = IntVar()
    var.set(vals[2])
    spin = Spinbox(window, from_=vals[0], to=vals[1], width=12, textvariable=var)
    spin.place(x=180, y=y_coord * multiplier)
    spins.append(spin)

txt = scrolledtext.ScrolledText(window, width=25, height=20)
txt.place(x=270, y=20)
btn = Button(window, text='Згенерувати і вивести', command=generate)
btn.place(x=40, y=300)


window.mainloop()
