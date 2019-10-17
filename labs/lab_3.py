from labs import *
from labs.md5 import MD5

from tkinter import *
from tkinter import messagebox
from tkinter.scrolledtext import *
from tkinter.filedialog import askopenfilename, asksaveasfilename


def generate_objects():
    pass


if __name__ == '__main__':

    window = create_window('LAB 3')
    generate_objects()

    user_input = ScrolledText(window, width=40, height=10)
    user_input.place(x=0, y=20)
    generated_md5 = ScrolledText(window, width=40, height=2)
    generated_md5.place(x=0, y=210)
    loaded_md5 = ScrolledText(window, width=40, height=2)
    loaded_md5.place(x=0, y=285)
    btn = Button(window, text='Згенерувати')
    btn.place(x=350, y=20)
    test_btn = Button(window, text='Тестувати')
    test_btn.place(x=350, y=50)
    btn = Button(window, text='Перевірити')
    btn.place(x=350, y=80)

    hasher = MD5()
    test_index = 0
    current_md5_file = None

    menubar = Menu(window)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Відкрити файл")
    filemenu.add_command(label='Відкрити MD5-файл')
    filemenu.add_separator()
    filemenu.add_command(label='Зберегти')
    filemenu.add_command(label='Зберегти як...')
    filemenu.add_separator()
    filemenu.add_command(label="Вийти", command=window.quit)
    menubar.add_cascade(label="Файл", menu=filemenu)

    window.config(menu=menubar)
    window.mainloop()

