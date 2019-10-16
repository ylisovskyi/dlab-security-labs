from tkinter import *
from tkinter import scrolledtext


window = Tk()

WIDTH = 500
HEIGHT = 400

multiplier = 25

window.title('Lab 2')
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
    (0, 2 ** 18 - 1, 1): 10
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
btn = Button(window, text='Згенерувати і вивести')
btn.place(x=40, y=300)


window.mainloop()
