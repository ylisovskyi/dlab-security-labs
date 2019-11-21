from labs import *
from labs.md5 import MD5
# from labs.rc5 import RC5
from labs.rc5_test import RC5

from tkinter import *
from tkinter import messagebox
from tkinter.scrolledtext import *
from tkinter.filedialog import askopenfilename, asksaveasfilename


def show_message_if_not_file(filename):
    if not filename:
        messagebox.showerror('Помилка завантаження файлу', 'Ви не обрали файл')
        return False

    return True


def set_hashed_key(secret):
    md5.set(secret)
    key = md5.digest()
    hashed.delete(0.0, END)
    hashed.insert(END, key)
    return key


def endecrypt(decrypt=True):
    w = int(spins[0].get())
    r = int(spins[1].get())
    b = int(spins[2].get())
    secret = user_input.get()
    key = set_hashed_key(secret)
    rc5 = RC5(w, r, b, key)
    func = rc5.decryptFile if decrypt else rc5.encryptFile
    infile = askopenfilename(
        parent=window,
        title='File to encrypt'
    )
    if not show_message_if_not_file(infile):
        return
    outfile = asksaveasfilename(
        parent=window,
        defaultextension='.txt',
        filetypes=[('Text document', '.txt')],
        title='File to write encrypted data to'
    )
    if not show_message_if_not_file(outfile):
        return
    func(
        inpFileName=infile,
        outFileName=outfile
    )


def generate_objects():
    place_labels(window, LAB_3_LABELS)
    return place_spins(window, LAB_3_SPINS, x=140, width=20)


if __name__ == '__main__':

    window = create_window('LAB 3')
    spins = generate_objects()

    user_input = Entry(window, width=22)
    user_input.place(x=140, y=75)
    hashed = ScrolledText(window, width=20, height=5)
    hashed.place(x=290, y=20)
    btn = Button(
        window, text='Зашифрувати файл', command=lambda: endecrypt(False)
    )
    btn.place(x=10, y=150)
    test_btn = Button(
        window, text='Дешифрувати файл', command=lambda: endecrypt()
    )
    test_btn.place(x=150, y=150)

    md5 = MD5()
    test_index = 0
    current_file = None

    menubar = Menu(window)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Відкрити файл")
    filemenu.add_separator()
    filemenu.add_command(label="Вийти", command=window.quit)
    menubar.add_cascade(label="Файл", menu=filemenu)

    window.config(menu=menubar)
    window.mainloop()

