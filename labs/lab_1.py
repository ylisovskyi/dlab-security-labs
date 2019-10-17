from labs import *

from tkinter import *
from tkinter import scrolledtext


def set_values():
    global a, m, c, rand, spins, count
    m = int(spins[0].get()) ** int(spins[1].get()) + int(spins[2].get())
    a = int(spins[3].get()) ** int(spins[4].get())
    c = int(spins[5].get())
    rand = int(spins[6].get())
    count = int(spins[7].get())


def generate():
    set_values()
    with open('out_lab_1.txt', 'w') as fp:
        txt.delete(0.0, END)
        txt.insert(END, str(rand) + '\n')
        fp.write(str(rand) + '\n')
        prev = None
        first = rand
        i, j = 0, 0
        while i < m:
            num = lcg()
            if j < count:
                txt.insert(END, str(num) + '\n')
            fp.write(str(num) + '\n')
            if (prev and num == prev) or num == first:
                period_label.config(text=str(j + 1))
                break
            prev = num
            j += 1


def lcg():
    global rand
    rand = (a * rand + c) % m
    return rand


def generate_objects():
    global spins
    place_labels(window, LAB_1_LABELS)
    spins = place_spins(window, LAB_1_SPINS)


if __name__ == '__main__':
    window = create_window('LAB 1')

    txt = scrolledtext.ScrolledText(window, width=25, height=20)
    btn = Button(window, text='Згенерувати і вивести', command=generate)
    period_label = Label(window, text='')

    txt.place(x=270, y=20)
    btn.place(x=40, y=300)
    period_label.place(x=360, y=14 * MULTIPLIER)

    generate_objects()
    window.mainloop()
