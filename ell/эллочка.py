from collections import deque
from math import pow

MIN_INT = -pow(2, 8)
MAX_INT = pow(2, 8) - 1
DEBUG = False
def dbg(**kwargs):
    for kw in kwargs:
        print(kw, ':', kwargs[kw])

def init_vars(cd=[], cls=[]):
    print('aaaaaaaaaa')
    print(cd)
    print(cls)

memory = [0 for i in range(30000)]
i = 0

'''

Начало программы:
    int[] = new int[30 000];

Список команд:

    команда                     эквивалент              описание

    Поедем на извозчике         i++                     перейти к следующей ячейке памяти
    Поедем на таксо             i--                     перейти к предыдущей ячейке памяти
    Мрак                        arr[i]++                увеличить значение в текущей ячейке на 1
    Жуть                        arr[i]--                уменьшить значение в текущей ячейке на 1
    Хо-хо!                      print(chr(arr[i]))      вывести символ из текущей ячейки в консоль (по коду UTF-8)
    Хамите                      arr[i] = ord(input())   ввести символ из консоли в текущую ячейку (по коду UTF-8)
-   Подумаешь!                  arr[i] = 0              обнулить значение текущей ячейки
        n Команда                                       повторить команду n раз
    Парниша A                   label A                 заголовок для условного перехода (Как ребёнка A перейдёт на эту строку). Пожалуйста, учитывайте, что Эллочка не учитывает регистры (Если в программе сначала встретится Парниша сюда, а потом Парниша Сюда, то второй заголовок заменит первый)
    Как ребёнка A               if (arr[i]) goto A      условный переход (переходит к строке Парниша A, если значение в текущей ячейке != 0)
        / ...                                           комментарий (символ / должен быть первым печчатаемым символом в строке)
    У вас вся спина белая       arr[i] = int(input())   ввести целое число в текущую ячейку из консоли
    Ого!                        print(arr[i])           вывести целое число из текущей ячейки в консоль
    Знаменито n                 arr[i] = arr[n]         записать значение ячейки на n правее текущей в текущую ячейку
'''


def nxt():
    global i
    if i + 1 > 29999:
        i = 0
    else:
        i += 1

def prv():
    global i
    if i - 1 < 0:
        i = 29999
    else:
        i -= 1

def plus():
    global i
    global memory
    if memory[i] + 1 > MAX_INT:
        memory[i] = MIN_INT
    else:
        memory[i] += 1

def minus():
    global i
    global memory
    if memory[i] - 1 < MIN_INT:
        memory[i] = MAX_INT
    else:
        memory[i] -= 1

def prnt():
    global i
    global memory
    print(chr(memory[i]), end='')

def inp():
    global i
    global memory
    try:
        memory[i] = ord(input())
    except:
        raise Exception('Not UTF-8 input')

def zero():
    global i
    global memory
    memory[i] = 0

def ifdef():
    global i
    global memory
    return memory[i] != 0

def inp_int():
    global i
    global memory
    st = input()
    try:
        memory[i] = int(st)
    except ValueError:
        raise ValueError(string.format('{0} невозможно преобразовать в целое число', st))

def prnt_int():
    global i
    global memory
    print(memory[i])

def into(c):
    global i
    global memory
    a = i + c
    if a > 29999:
        while a > 29999:
            a -= 29999
    elif a < 0:
        while a < 29999:
            a += 29999
    memory[i] = memory[a]

FUNCS = {
    'поедем на извозчике': nxt,
    'поедем на таксо': prv,
    'мрак': plus,
    'жуть': minus,
    'хо-хо!': prnt,
    'хамите': inp,
    'подумаешь!': zero,
    'у вас вся спина белая': inp_int,
    'ого!': prnt_int
    }

def parse(code: str):
    calls = deque()
    
    code = code.splitlines()

    jump = -1
    
    for j in range(len(code)):
        string = code[j].strip().lower()

        if jump > 0 and j <= jump:
            continue
            
        if string == '' or string[0] == '/':
            continue
        
        elif string[0].isnumeric():
            try:
                n = int(string.split(' ')[0])
            except ValueError:
                raise SyntaxError('Количество повторов команды должно быть целым числом')
            command = ' '.join(string.split(' ')[1::])
            for j in range(n):
                try:
                    calls.appendleft(FUNCS[command])
                except KeyError:
                    raise SyntaxError(str.format('Неизвестная команда: {0}', command))

        elif string.startswith('парниша'):
            calls.appendleft(str('>' + string[7::]))

        elif string.startswith('как ребёнка'):
            calls.appendleft(str('<' + string[11::]))

        elif string.startswith('знаменито'):
            calls.appendleft(str('=' + string[9::]))
                
        else:
            try:
                calls.appendleft(FUNCS[string])
            except KeyError:
                raise SyntaxError(str.format('Неизвестная команда: {0}', string))

    return calls


def main(file_n=None):
    global DEBUG

    if file_n:
        filename = file_n
        file = open(filename, 'r')
    else:
        while True:
            filename = input('введите имя файла с программой: ')
            try:
                file = open(filename, 'r')
                break
            except FileNotFoundError:
                pass

    code = file.read()
    calls = parse(code)
    calls.reverse()

    with open(filename + '.log', 'w') as f:
        f.write('сформирована последовательность команд:\n')
        for fnc in calls:
            if isinstance(fnc, str):
                f.write(fnc + '\n')
            else:
                f.write(fnc.__name__ + '\n')

    if DEBUG:
        init_vars(cd=code, cls=calls)
            
    j = 0
    labels = {}

    if DEBUG:
        dbg(i=i, memory=memory, curr_cell=memory[i], command='', calls=calls, j=j)
    
    while j < len(calls):
        command = calls[j]
        if isinstance(command, str):
            if command[0] == '>':
                labels.update({command[1::]: j})
                j += 1
            elif command[0] == '<':
                if ifdef():
                    try:
                        j = labels[command[1::]]
                    except KeyError:
                        with open(filename + '.log', 'a') as f:
                            f.write(str.format('\n!! условный переход на несуществующий заголовок {0} !!\t эта строка пропущена', command[1::]))
                        j += 1
                else:
                    j += 1
            elif command[0] == '=':
                c = command[1::]
                try:
                    cell = int(c)
                except ValueError:
                    raise SyntaxError(str.format('После "Знаменито" через пробел должно быть целое число, а не {0}', c))
                into(cell)
                j += 1
            else:
                raise SyntaxError(str.format('В очередь вызовов добавлена неизвестная строка {0}', command))

        else:
            command()
            j += 1

        if DEBUG:
            dbg(i=i, memory=memory, curr_cell=memory[i], command=command, calls=calls, j=j)
            
    #input()

if __name__ == '__main__':
    main()

def run(debug_func=None, init_vars_func=None, file=None):
    global DEBUG
    global dbg
    global init_vars
    
    if debug_func:
        DEBUG = True
        dbg = debug_func
        if init_vars_func:
            init_vars = init_vars_func
    main(file)



        
