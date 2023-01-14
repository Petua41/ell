# Programming language "Ellochka"
Further -- in Russian. I'll translate it later

## Описание
"Эллочка" -- язык программирования, составленный из фраз Эллочки-Людоедки из романа "12 стульев"

## Файлы
* **constructor.py** -- среда разработки (IDE слишком громко сказано) для "Эллочки". По сути, это просто текстовое поле, кнопки "Сохранить-Загрузить" и список, из которого можно встывить команду, если боитесь ошибиться, пока вписываете её руками. *Красиво выделяет команды синеньким!*
* **custom_text.py** -- технический файл, нужен для красивого выделения команд синеньким
* **debugger.py** -- что-то типа дебаггера для "Эллочки". Позволяет выполнять программу по шагам, отображает ленту (память), исходный код программы (только в ознакомительных целях, редактировать нельзя) и текст программы на "Эллочка-ассемблере"
* **translator_c.py** -- транслирует программу на "Эллочке" в C. С помощью GCC копмилирует её. Генерирует исполняемый файл и кучу мусора (свои логи, логи от GCC, \*.c и т. д.)
* **эллочка.py** -- интерпретатор "Эллочки"
* **Спецификация.docx** -- спецификация. Если **вдруг** Вы захотите на писать свою реализацию "Эллочки". Я переведу её в Markdown. Обещаю

У транслятора и интерпретатора уродлявый интерфейс командной строки, так что лучше запускайте их с помощью специальных кнопок в IDE. Остальные программы написаны на tkinter с темой Breeze (моя любимая), так что у них приятный дизайн даже на Виндах.
