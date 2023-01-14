from collections import deque
from os import system

'''MIN_INT = - 2 ** 8
MAX_INT = 2 ** 8 - 1

memory = [0 for i in range(30000)]
i = 0'''


class GCCError(Exception):
    def __init__(self, msg='Неизвестная ошибка gcc'):
        super.__init__(self, msg=str.format('Ошибка gcc:{0}\nСкорее всего, gcc не установлен или не добавлен в PATH', msg))


beg = '''#include <stdio.h>
int main()
{
short i = 0;
short arr[3000] = {0};
char ch;
'''

fin = '''system("pause");
return 0;
}'''

'''def nxt():
    global i
    if i + 1 > 29999:
        i = 0
    else:
        i += 1'''

nxt = 'if (i == 29) i = 0; else i ++;\n'

'''def prv():
    global i
    if i - 1 < 0:
        i = 29999
    else:
        i -= 1'''

prv = 'if (i == 0) i = 29; else i --;\n'

'''def plus():
    global i
    global memory
    if memory[i] + 1 > MAX_INT:
        memory[i] = MIN_INT
    else:
        memory[i] += 1'''

pls = 'arr[i]++;\n'

'''def minus():
    global i
    global memory
    if memory[i] - 1 < MIN_INT:
        memory[i] = MAX_INT
    else:
        memory[i] -= 1'''

mns = 'arr[i]--;\n'

'''def prnt():
    global i
    global memory
    print(chr(memory[i]), end='')'''

pch = 'printf("%c", arr[i]);\n'

'''def inp():
    global i
    global memory
    try:
        memory[i] = ord(input())
    except:
        raise Exception('Not UTF-8 input')'''

ich = 'scanf("%c", &arr[i]);\n'

'''def zero():
    global i
    global memory
    memory[i] = 0'''

zer = 'arr[i] = 0;\n'

def ifdef():
    global i
    global memory
    return memory[i] != 0

'''def inp_int():
    global i
    global memory
    st = input()
    try:
        memory[i] = int(st)
    except ValueError:
        raise ValueError(string.format('{0} невозможно преобразовать в целое число', st))'''

iit = '''scanf("%s", &ch);
arr[i] = strtol(&ch, NULL, 10);
'''

def prnt_int():
    global i
    global memory
    print(memory[i])

pit = 'printf("%d", arr[i]);\n'

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

def mov(x):
    c = int(x)
    if c >= 30000:
        c %= 30000
    elif c <= -30000:
        while c <= -3000:
            c += 30000
    return str.format('''if (i + {0} >= 30000) arr[i] = arr[i + {0} - 30000];
else if (i + {0} < 0) arr[i] = arr[i + {0} + 30000];
else arr[i] = arr[i + {0}];
''', c)

lbl = lambda x: str.format('{0}:\n', x)
gto = lambda x: str.format('if (arr[i] != 0) goto {0};\n', x)

FUNCS = {
    'поедем на извозчике': 'nxt',
    'поедем на таксо': 'prv',
    'мрак': 'pls',
    'жуть': 'mns',
    'хо-хо!': 'pch',
    'хамите': 'ich',
    'подумаешь!': 'zer',
    'у вас вся спина белая': 'iit',
    'ого!': 'pit'
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


def main(filename=None):
    if filename:
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
            
    j = 0
    labels = {}

    filename = filename.split('.')[0]
    f = open(str.format('{0}.c', filename), 'w')
    f.write(beg)
    
    while j < len(calls):
        command = calls[j]
        if isinstance(command, str):
            '''if command[0] == '>':
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
                raise SyntaxError(str.format('В очередь вызовов добавлена неизвестная строка {0}', command))'''

            match command:
                case 'nxt':
                    f.write(nxt)
                case 'prv':
                    f.write(prv)
                case 'pls':
                    f.write(pls)
                case 'mns':
                    f.write(mns)
                case 'pit':
                    f.write(pit)
                case 'pch':
                    f.write(pch)
                case 'ich':
                    f.write(ich)
                case 'zer':
                    f.write(zer)
                case 'iit':
                    f.write(iit)
                case _:             # > и <
                    if command.startswith('>'):
                        f.write(lbl(command[1::]))
                    elif command.startswith('<'):
                        f.write(gto(command[1::]))
                    elif command.startswith('='):
                        f.write(mov(command[1::]))
                    else:
                        raise SyntaxError('В очередь вызовов попала неизвестная команда ' + command)
                    
            j += 1

    f.write(fin)
    f.close()

    err = system(str.format('gcc {0}.c -o {0}', filename))
    if err:
        raise GCCError()

if __name__ == '__main__':
    main()



        
