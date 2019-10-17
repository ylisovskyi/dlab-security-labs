from labs import *
from labs.md5 import MD5

from tkinter import *
from tkinter import messagebox
from tkinter.scrolledtext import *
from tkinter.filedialog import askopenfilename, asksaveasfilename


def process(data=None):
    generated_md5.delete(0.0, END)
    data = data or user_input.get(1.0, END)[:-1]
    hasher.set(data)
    result = hasher.hexdigest().upper()
    generated_md5.insert(END, result)
    return result


def test():
    global test_index, is_correct_label
    test_data, expected = list(LAB_2_TEST_SET.items())[test_index]
    user_input.delete(0.0, END)
    user_input.insert(END, test_data)
    actual = process(test_data)
    test_index = 0 if test_index + 1 == len(LAB_2_TEST_SET) else test_index + 1
    correct = 'Так' if actual == expected else 'Ні'
    is_correct_label.config(text=correct)


def generate_objects():
    global is_correct_label
    labels = place_labels(window, LAB_2_LABELS)
    is_correct_label = labels[-1]


def process_file():
    tmp_hasher = MD5()
    user_input.delete(0.0, END)
    filename = askopenfilename(parent=window)
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            tmp_hasher.update(chunk)
    result = tmp_hasher.hexdigest().upper()
    generated_md5.delete(0.0, END)
    generated_md5.insert(END, result)


def load_md5_file():
    global current_md5_file
    loaded_md5.delete(0.0, END)
    filename = askopenfilename(parent=window)
    with open(filename, 'r') as f:
        md5 = f.read()
        loaded_md5.insert(END, md5)
    current_md5_file = filename


def save_file():
    md5 = generated_md5.get(0.0, END)[:-1]
    if current_md5_file is not None:
        with open(current_md5_file, 'w') as f:
            f.write(md5)
    else:
        save_as()


def save_as():
    filename = asksaveasfilename(parent=window)
    md5 = generated_md5.get(0.0, END)[:-1]
    with open(filename, 'w') as f:
        f.write(md5)


def check_loaded():
    generated = generated_md5.get(0.0, END)[:-1]
    loaded = loaded_md5.get(0.0, END)[:-1]
    if not generated or not loaded:
        messagebox.showerror(
            'Помилка введення',
            'Ви не завантажили або не згенерували MD5. Спробуйте ще раз'
        )
    else:
        correct = 'Так' if generated == loaded else 'Ні'
        is_correct_label.config(text=correct)


if __name__ == '__main__':

    window = create_window('LAB 2')
    generate_objects()

    user_input = ScrolledText(window, width=40, height=10)
    user_input.place(x=0, y=20)
    generated_md5 = ScrolledText(window, width=40, height=2)
    generated_md5.place(x=0, y=210)
    loaded_md5 = ScrolledText(window, width=40, height=2)
    loaded_md5.place(x=0, y=285)
    btn = Button(window, text='Згенерувати', command=process)
    btn.place(x=350, y=20)
    test_btn = Button(window, text='Тестувати', command=test)
    test_btn.place(x=350, y=50)
    btn = Button(window, text='Перевірити', command=check_loaded)
    btn.place(x=350, y=80)

    hasher = MD5()
    test_index = 0
    current_md5_file = None

    menubar = Menu(window)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Відкрити файл", command=process_file)
    filemenu.add_command(label='Відкрити MD5-файл', command=load_md5_file)
    filemenu.add_separator()
    filemenu.add_command(label='Зберегти', command=save_file)
    filemenu.add_command(label='Зберегти як...', command=save_as)
    filemenu.add_separator()
    filemenu.add_command(label="Вийти", command=window.quit)
    menubar.add_cascade(label="Файл", menu=filemenu)

    window.config(menu=menubar)
    window.mainloop()
