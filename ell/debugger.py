import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import эллочка as ell
from threading import Thread
from os import fsencode

ttkthemes_imported = True

try:
    from ttkthemes import ThemedTk
except ModuleNotFoundError:
    ttkthemes_imported = False


class Debugger():
    def __init__(self):
        self.sel_acts = []
        self.send_to_run = {
            'debug_func': self.act,
            'init_vars_func': self.init_vars,
            'file': None
            }
        
        self.mode_select()

    def file_select(self):
        file = filedialog.askopenfilename()
        try:
            open(file, 'r')
        except FileNotFoundError:
            return False
        self.send_to_run['file'] = file
        return True

    def mode_select(self, file=None):
        self.all_actions_descs = {
            'curr_cell': 'Значение в текущей ячейке',
            'memory_f': '20 ячеек вокруг текущей',
            'calls_f': '10 команд вокруг той, которая сейчас выполняется',
            'code_f': 'Исходный код'
            }
        self.all_actions_funcs = {
            'curr_cell': self.curr_cell,
            'memory_f': self.memory_f,
            'calls_f': self.calls_f,
            'code_f': self.code_f
            }

        if ttkthemes_imported:
            root = ThemedTk(theme='breeze')
        else:
            root = tk.Tk()
            messagebox.showwarning(message='Нужно установить ttkthemes\nОткройте IDE, чтобы установить', title='Нет модуля')
        root.focus_force()
        root.title('[configure] DEBUG')
        
        frm_chb = ttk.Frame(root, padding=20, borderwidth=1, relief='sunken')
        frm_chb.grid(row=0, columnspan=2)

        frm_fsb = ttk.Frame(root, padding=20)
        frm_fsb.grid(row=1, column=0)

        frm_b = ttk.Frame(root, padding=20)
        frm_b.grid(row=1, column=1)

        self.file_selected = False
        def butt_pressed():
            if not len(self.sel_acts):
                return
            root.destroy()
            self.start_real_init()

        def fsbutton():
            self.file_selected = self.file_select()
            if self.file_selected:
                fsbutt['text'] = 'Файл выбран'
            if len(self.sel_acts) and self.file_selected:
                btn['state'] = ['normal']
                btn['text'] = 'Start'
            else:
                btn['state'] = ['disabled']
                if len(self.sel_acts):
                    btn['text'] = 'Выберите файл'
                elif self.file_selected:
                    btn['text'] = 'Выберите режим'
                else:
                    btn['text'] = 'Выберите режим и файл'

        fsbutt = ttk.Button(frm_fsb, text='Выбрать файл', command=fsbutton)
        fsbutt.pack()

        btn = ttk.Button(frm_b, text='Выберите режим и файл', command=butt_pressed, state=['disabled'])
        btn.pack()
        
        self.sel_acts =[]

        def select():
            self.sel_acts = []
            #if curr_cell.get() == 1: result.append('curr_cell')
            if memory_f.get() == 1: self.sel_acts.append('memory_f')
            if calls_f.get() == 1: self.sel_acts.append('calls_f')
            if code_f.get() == 1: self.sel_acts.append('code_f')
            if len(self.sel_acts) and self.file_selected:
                btn['state'] = ['normal']
                btn['text'] = 'Start'
            else:
                btn['state'] = ['disabled']
                if len(self.sel_acts):
                    btn['text'] = 'Выберите файл'
                elif self.file_selected:
                    btn['text'] = 'Выберите режим'
                else:
                    btn['text'] = 'Выберите режим и файл'
         
        position = {"padx":6, "pady":6, "anchor":tk.NW}
         
        #curr_cell = tk.IntVar()
        #ttk.Checkbutton(frm_chb, text='Значение в текущей ячейке', variable=curr_cell, command=select).pack(**position)
        
        memory_f = tk.IntVar()
        ttk.Checkbutton(frm_chb, text='20 ячеек вокруг текущей', variable=memory_f, command=select).pack(**position)
        
        calls_f = tk.IntVar()
        ttk.Checkbutton(frm_chb, text='10 команд вокруг той, которая сейчас выполняется', variable=calls_f, command=select).pack(**position)
        
        code_f = tk.IntVar()
        ttk.Checkbutton(frm_chb, text='Исходный код', variable=code_f, command=select).pack(**position)
        
        root.mainloop()

    def start_real_init(self):
        try:
            self.actions = [self.all_actions_funcs[action] for action in self.sel_acts]
        except KeyError as ex:
            raise ValueError('[DEBUGGER] Unknown action\n' + ex)
        self.real_init()
    
    def real_init(self):
        self.code = []
        self.calls = []
        self.flag = True
        self.running = False

        if ttkthemes_imported:
            self.root = ThemedTk(theme='breeze')
        else:
            self.root = tk.Tk()
        self.root.focus_force()
        self.root.title('DEBUG')
        
        self.frm_b = ttk.Frame(self.root, padding=20)
        self.frm_b.grid(row=2, columnspan=2)
        self.frm_m = ttk.Frame(self.root, padding=20, borderwidth=1, relief='sunken')
        self.frm_m.grid(row=0, columnspan=2)
        self.frm_c = ttk.Frame(self.root, padding=20, borderwidth=1, relief='sunken')
        self.frm_c.grid(column=0, row=1)
        self.frm_code = ttk.Frame(self.root, padding=20)
        self.frm_code.grid(column=1, row=1)
        
        self.btn = ttk.Button(self.frm_b, text='Step', command=self.resume)
        self.btn.grid()

        '''if self.curr_cell in self.actions:
            self.lbl = ttk.Label(self.frm_m, text='__')
            self.lbl.grid()'''

        if self.memory_f in self.actions:
            self.mem_lbls = []
            for j in range(20):
                label = ttk.Label(self.frm_m, text = '_')
                label.grid(column=2 * j, row=0)
                space = ttk.Label(self.frm_m, text = ' ')
                space.grid(column=2 * j + 1, row=0)
                self.mem_lbls.append(label)

        if self.calls_f in self.actions:
            self.calls_lbls = []
            for j in range(10):
                label = ttk.Label(self.frm_c, text=' ')
                label.grid(column=0, row=j)
                self.calls_lbls.append(label)
                
        if self.code_f in self.actions:
            self.txt = tk.Text(self.frm_code)
            self.txt.grid()
            self.txt['height'] = 15
            self.txt['width'] = 25
            self.txt_inited = False

        self.thread = Thread(target=ell.run, kwargs=self.send_to_run)
        self.thread.start()
        self.running = True
        self.root.title('[running] DEBUG')
        
        self.root.mainloop()
        
    def init_vars(self, cd=[], cls=[]):
        self.code = list(map(lambda x: x.strip(), filter(lambda x: x.isprintable() and len(x), cd.split('\n'))))
        self.calls = list(cls)

    def resume(self):
        self.running = self.thread.is_alive()

        if not self.running:
            self.root.title('[finished] DEBUG')
            self.term()
            return
        
        self.flag = False

    def curr_cell(self, kwargs):
        self.lbl['text'] = kwargs['curr_cell']

    def memory_f(self, kwargs):
        memory = kwargs['memory']
        i = kwargs['i']
        if i <= 10 or len(memory) - i <= 5:
            show_mem = memory[:20:]
            idx = i
        else:
            show_mem = memory[i - 10:i + 10:]
            idx = 10

        for i in range(20):
            self.mem_lbls[i]['text'] = show_mem[i]
            self.mem_lbls[i]['background'] = ''
            if i == idx:
                self.mem_lbls[i]['background'] = '#00F000'

    def calls_f(self, kwargs):
        calls_j = kwargs['j']
        if calls_j <= 5 or len(self.calls) - calls_j <= 5:
            show_calls = self.calls[:10:]
            calls_idx = calls_j
        else:
            show_calls = self.calls[calls_j - 5:calls_j + 5:]
            calls_idx = 5

        
        for j in range(10):
            self.calls_lbls[j]['text'] = (show_calls[j] if isinstance(show_calls[j], str) else show_calls[j].__name__)
            self.calls_lbls[j]['background'] = ''
            if j == calls_idx:
                self.calls_lbls[j]['background'] = '#00FF00'

    def code_f(self, kwargs):
        if not self.txt_inited:
            self.txt.insert('1.0', '\n'.join(self.code))
            self.txt['state'] = ['disabled']
            self.txt_inited = True

    def act(self, **kwargs):
        self.flag = True

        for action in self.actions:
            action(kwargs)

        while self.flag:
            pass

    def term(self):
        if self.running:
            raise RuntimeError('Вызван Debugger.term, но Эллочка ещё работает')
        self.btn['text'] = 'Close'
        self.btn['command'] = self.root.destroy

def main():
    dbgr = Debugger()

if __name__ == '__main__':
    main()


