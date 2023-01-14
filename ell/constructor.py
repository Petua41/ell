from tkinter import *
from tkinter import ttk, filedialog, messagebox
from _tkinter import TclError
from threading import Thread
import эллочка as ell
import translator_c
from custom_text import CustomText
from os import system

ttkthemes_imported = True

try:
    from ttkthemes import ThemedTk
    from debugger import main as debug_main
except ModuleNotFoundError:
    ttkthemes_imported = False

filename = None
file_saved = True
 
def del_btn_default_text():
    del_btn['text'] = 'Удалить'

def close():
    if not file_saved:
        answer = messagebox.askyesnocancel(message='Сохранить файл перед выходом?', title='Сохранить?')
        match answer:
            case True:
                save()
                root.destroy()
            case False:
                root.destroy()
            case None:
                return
            case _:
                raise Exception('YesNoCancel Dialog вернул неизвестное значение')
    else:
        root.destroy()

def debug():
    #if not ttkthemes_imported:
        #messagebox.showerror(title='нет модуля', message='Невозможно запустить дебаггер без модуля ttkthemes')
    root.destroy()
    debug_main()

def run():
    if not file_saved:
        answer = messagebox.askokcancel(message='File must be saved before run\nSave?', title='Save?')
        if answer:
            save()
        else:
            return
    ell_thread = Thread(target=ell.run, kwargs={'file': filename})
    ell_thread.start()

def translate():
    if not file_saved:
        answer = messagebox.askokcancel(message='File must be saved before run\nSave?', title='Save?')
        if answer:
            save()
        else:
            return
    ell_thread = Thread(target=translator_c.main, kwargs={'filename': filename})
    ell_thread.start()
 
# добавление нового элемента
def add():
    new_cmd = '' if (len(code_txt.get(0.0, 'end')) < 2 or code_txt.get(0.0, 'end')[-2] == '\n') else '\n'
    if count.get() == '1':
        new_cmd += cmd_var.get()
    else:
        new_cmd += count.get() + ' ' + cmd_var.get()

    if len(goto_var.get()) > 0:
        new_cmd += ' ' + goto_var.get()
    elif len(loop_count.get()) > 0:
        new_cmd += ' ' + loop_count.get()
    
    new_cmd += '\n'
    code_txt.insert(END, new_cmd)
    
    on_modified(None)

def on_modified(event):
    global file_saved
    
    if len(code_txt.get(0.0, 'end')) > 0 and not code_txt.get(0.0, 'end').isspace():
        save_btn['state'] = ['normal']
    else:
        save_btn['state'] = ['disabled']

    edit_menu.entryconfigure(edit_menu.index('Назад'), state=['normal'])

    highlight_syntax()

    root.title('*CONSTRUCTOR*')
    file_saved = False

def highlight_syntax():
    code_txt.tag_delete('syntax', 0.0, 'end')
    code_txt.tag_configure('syntax', foreground='#0000FF')
    for word in highlight_words:
        code_txt.highlight_pattern(word, 'syntax')

def undo():
    try:
        code_txt.edit_undo()
        edit_menu.entryconfigure(edit_menu.index('Вперёд'), state=['normal'])
    except TclError:
        raise Exception('Nothing to undo')
    try:
        code_txt.edit_undo()
        code_txt.edit_redo()
    except TclError:
        edit_menu.entryconfigure(edit_menu.index('Назад'), state=['disabled'])

def redo():
    try:
        code_txt.edit_redo()
        edit_menu.entryconfigure(edit_menu.index('Назад'), state=['normal'])
    except TclError:
        raise Exception('Nothing to redo')
    try:
        code_txt.edit_redo()
        code_txt.edit_undo()
    except TclError:
        edit_menu.entryconfigure(edit_menu.index('Вперёд'), state=['disabled'])

def save_as():
    global filename
    
    filename = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[('Текстовый файл', '.txt'), ('Исходный код Эллочки', '.ell')])
    try:
        file = open(filename, 'w')
    except FileNotFoundError:
        messagebox.showwarning(message='Не удалось сохранить файл.\nПопробуйте ещё раз', title='WARNING')
        return
    if file == None:
        return
    save()

def save():
    global filename
    global file_saved

    if filename == None:
        save_as()
    else:
        file = open(filename, 'w')
        file.write(code_txt.get(0.0, 'end').strip())
        file.close()

    root.title('CONSTRUCTOR')
    file_saved = True

def open_file():
    global filename
    global file_saved

    if not file_saved:
        answer = messagebox.askyesnocancel(message='Сохранить старый файл перед открытием нового?', title='Сохранить?')
        match answer:
            case True:
                save()
            case False:
                pass
            case None:
                return
            case _:
                raise Exception('YesNoCancel Dialog вернул неизвестное значение')

    filename = filedialog.askopenfilename(filetypes=[('Текстовый файл', '.txt'), ('Исходный код Эллочки', '.ell'), ('Все файлы', '.*')])
    try:
        file = open(filename)
        code_txt.delete(0.0, 'end')
        code_txt.insert(0.0, file.read())
        on_modified(event=None)
        file_saved = True
        root.title('CONSTUCTOR')
    except FileNotFoundError:
        messagebox.showwarning(title='WARNING', message='Не удалось открыть файл')

def select_command(event=None):
    global spnbx_loop_count
    global goto_entry

    try:
        loop_count.set('')
        spnbx_loop_count.destroy()
    except TclError:
        pass

    try:
        goto_var.set('')
        goto_entry.destroy()
    except TclError:
        pass
    
    if cmd_var.get() == 'Парниша' or cmd_var.get() == 'Как ребёнка':
        goto_var.set('A')
        goto_entry = ttk.Entry(frm_top, textvariable=goto_var, width=6)
        goto_entry.grid(row=0, column=3)
        
    elif cmd_var.get() == 'Знаменито':
        loop_count.set('1')
        spnbx_loop_count = ttk.Spinbox(frm_top, from_=1, to=999, width=4, textvariable=loop_count, state=['readonly'])
        spnbx_loop_count.grid(row=0, column=3)

if ttkthemes_imported:
    root = ThemedTk(theme='breeze')
else:
    root = Tk()
    if messagebox.showwarning(message='Нужно установить ttkthemes\nУстановить?', title='Нет модуля'):
        err_code = system('pip install ttkthemes')
        if err_code:
           messagebox.showerror(title='ERROR', message='Не удалось установить ttkthemes')
        else:
            messagebox.showinfo(title='модуль установлен', message='Модуль ttkthemes установлен.\nЧтобы применить изменения, перезапустите CONSTRUCTOR')
root.title("CONSTRUCTOR")

frm_top = ttk.Frame(root, padding=10)
frm_top.grid(row=0)
frm_mid = ttk.Frame(root, padding=10)
frm_mid.grid(row=1)
frm_bottom = ttk.Frame(root, padding=5)
frm_bottom.grid(row=2)

count = StringVar(value='1')
spnbx_count = ttk.Spinbox(frm_top, from_=1, to=999, width=4, textvariable=count, state=['readonly'])
spnbx_count.grid(row=0, column=0)

loop_count = StringVar(value='1')
spnbx_loop_count = ttk.Spinbox(frm_top, from_=1, to=999, width=4, textvariable=loop_count, state=['readonly'])

goto_var = StringVar(value='A')
goto_entry = ttk.Entry(frm_top, textvariable=goto_var, width=6)

commands_descs = {
    'Поедем на извозчике': 'перейти к следующей ячейке памяти',
    'Поедем на таксо': 'перейти к предыдущей ячейке памяти',
    'Мрак': 'увеличить значение в текущей ячейке на 1',
    'Жуть': 'уменьшить значение в текущей ячейке на 1',
    'Хо-хо!': 'вывести символ из текущей ячейки в консоль (по коду UTF-8)',
    'Хамите':  'ввести символ из консоли в текущую ячейку (по коду UTF-8)',
    'Подумаешь!': 'обнулить значение текущей ячейки',
    'Парниша': 'заголовок для условного перехода (Как ребёнка A перейдёт на эту строку). Регистр не учитывается',         # str
    'Как ребёнка': 'условный переход (переходит к строке Парниша A, если значение в текущей ячейке != 0)',                # str
    'У вас вся спина белая': 'ввести целое число в текущую ячейку из консоли',
    'Ого!': 'вывести целое число из текущей ячейки в консоль',
    'Знаменито': 'записать значение ячейки на n правее текущей в текущую ячейку'                                          # int
    }

highlight_words = ['поедем на извозчике', 'поедем на таксо', 'мрак', 'жуть', 'хо-хо!', 'хамите', 'подумаешь!', 'парниша', 'как ребёнка', 'у вас вся спина белая', 'ого!', 'знаменито',
                   'Поедем на извозчике', 'Поедем на таксо', 'Мрак', 'Жуть', 'Хо-хо!', 'Хамите', 'Подумаешь!', 'Парниша', 'Как ребёнка', 'У вас вся спина белая', 'Ого!', 'Знаменито']

cmd_var = StringVar(value='Поедем на извозчике')
cmd = ttk.Combobox(frm_top, values=list(commands_descs.keys()), state=['readonly'], textvariable=cmd_var, width=20) #, command=select_command)
cmd.grid(row=0, column=1, columnspan=2)
cmd.bind('<<ComboboxSelected>>', select_command)

add_btn = ttk.Button(frm_top, text="Добавить", command=add)
add_btn.grid(row=1, column=1)

code_txt = CustomText(frm_mid, width=30, height=25, undo=True)
code_txt.pack()
code_txt.bind('<KeyRelease>', on_modified)

save_btn = ttk.Button(frm_bottom, text='Сохранить', state=['disabled'], command=save)
save_btn.grid(row=0, column=0)

root.option_add("*tearOff", FALSE)

file_menu = Menu()
file_menu.add_command(label='Сохранить', command=save)
file_menu.add_command(label='Сохранить как...', command=save_as)
file_menu.add_command(label='Открыть...', command=open_file)
file_menu.add_separator()
file_menu.add_command(label='Выход', command=root.destroy)

edit_menu = Menu()
edit_menu.add_command(label='Назад', command=undo, state=['disabled'])
edit_menu.add_command(label='Вперёд', command=redo, state=['disabled'])

comp_menu = Menu()

comp_menu.add_command(label='Run', command=run)
comp_menu.add_command(label='Translate to C', command=translate)
comp_menu.add_separator()
comp_menu.add_command(label='Дебаггер...', command=debug)

main_menu = Menu()

main_menu.add_cascade(label='Файл', menu=file_menu)
main_menu.add_cascade(label='Edit', menu=edit_menu)
main_menu.add_cascade(label='Инструменты', menu=comp_menu)

root.config(menu=main_menu)

root.protocol("WM_DELETE_WINDOW", close)
 
root.mainloop()
