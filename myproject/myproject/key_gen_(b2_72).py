"""Генератор ключей/паролей (beta v.2.72)"""

# переменная key_string доступна при обращении к key_gen
import re  # Support for regular expressions (RE)
from random import random  # для генерации случайных чисел (необходимо)
import os  # для записи ключа в файл (при необходимости)
from pathlib import Path  # для вывода пути к файлу (при необходимости)
import string  # для получения списков (строк) символов (если писать лень)
import secrets  # для простой генерации ключа (идите в конец файла, где "if not use_file:", там применение)

COMMENTS = 1  # вывод пояснений в terminal для отладки
if COMMENTS:
    print(' -' * 5, 'Start output', '- ' * 80)

# ??импорт настроек при обращении...
# НАСТРОЙКИ ГЕНЕРАТОРА - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
k_type: int = 0  # 0 - только для copy/past (включает похожие символы), 1 - для ручного ввода (визуальное отличие)
k_len: int = 99  # Длинна строки символов (не больше чем...) (рекомендую 12 и более, uniq(E&R)(U&D)+sp1,2+.. (>4 веков))
# Ключи тестировались на https://password.kaspersky.com/ru/
use_eq_prob: int = 1  # 1 - равновероятное использование всех символов, иначе "вероятность" будет заданной
# Наборы символов: [название (просто для наглядности), вкл.(1)/выкл.(0), "вероятность"]
# Набор русских букв только для паролей (кодировка w-1251 плохо "переваривается")
used_chr_sets = [['eng', 1, 1], ['rus', 0, 1], ['dig', 1, 1], ['sp1', 1, 0.9], ['sp2', 1, 0.8], ['sp3', 0, 0.7]]
excluded: str = ' '  # список исключенных символов (сейчас только "пробел")
# 'eng' - английский алфавит, 'rus' - русский алфавит, dig' - цифры (десятичная система, можно и другую на их основе)
# 'sp1' - символы ~@#$%^-_(){}'`(могут использоваться в коротких и длинных именах файлов)
# 'sp2' - символы +=[] ;,.      (есть "пробел")(не могут использоваться в коротких именах файлов, но могут в длинных)
# 'sp3' - символы |/\:<>        (вообще не могут использоваться в именах файлов)
use_up_c = 1  # ABC/АБВ, (по умолчанию все символы в UpCase)
use_lw_c = 1  # abc/абв, включение строчных символов (без use_up_c = 1 будут только они)
# при установке обоих use_??_c в 0 будет применено use_up_c = 1
use_block = 0  # формат вида XXXX-XXXX-XXXX, рекомендуется только для ключа из букв и цифр, знаки "-" - часть ключа
num_block = 5  # число символов в блоке, рекомендуется от 3 до 8 (если блочность вообще включена)
# параметры относящиеся к записи ключа в файл
use_file = 1  # 1 - запись ключа в файл
file_name = 'gen_key.py'  # будет создан в текущей директории (для вывода пояснений нужен comments = 1)
overwrite_file = 0  # перезапись файла (если вывод в него): 1 - разрешить (не рекомендуется), 0 - запретить
# Изменять SECRET_KEY в Django проекте при каждом рестарте сервера плохая идея? (https://qna.habr.com/q/762193)
# Настройка Django Settings: лучшие практики: https://webdevblog.ru/nastrojka-django-settings-luchshie-praktiki/
use_infile = 1  # использовать оформление строки key_string в файле (настройки для примера), иначе только запись ключа
if use_infile:
    excluded += "'" + '"'  # по усмотрению
infile_prefix = "SECRET_KEY = '"  # перед key_string
infile_ending = "'"  # после key_string
# КОНЕЦ НАСТРОЕК - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

use_block = int(bool(use_block))
use_eq_prob = int(bool(use_eq_prob))
if not (use_up_c or use_lw_c):
    use_up_c = 1
eng_set = ['ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'DFGIJLNQSUVWZ', 'AbCcdEFGHhJLoPrUY']
rus_set = ['АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ', 'БГДЁЖЗИЛФЦЧШЬЭЮЯ', 'АГЕНПРСУЭ']
full_list = [[used_chr_sets[0][1] * use_up_c, used_chr_sets[0][2], eng_set[k_type]],
             [used_chr_sets[0][1] * use_lw_c, used_chr_sets[0][2], eng_set[k_type].lower()],
             [used_chr_sets[1][1] * use_up_c, used_chr_sets[1][2], rus_set[k_type]],
             [used_chr_sets[1][1] * use_lw_c, used_chr_sets[1][2], rus_set[k_type].lower()],
             [used_chr_sets[2][1], used_chr_sets[2][2],            '0123456789'],
             [used_chr_sets[3][1], used_chr_sets[3][2],            r"~@#$%^-_(){}'`"],
             [used_chr_sets[4][1], used_chr_sets[4][2],            r"+=[] ;,."],
             [used_chr_sets[5][1], used_chr_sets[5][2],            r"\/:*?<>|"]]
pna = [2]  # список простых чисел (для выбора при генерации случайных чисел вероятно излишен, но пусть будет)
for t_cou in range(3, 1000, 2):
    flag: int = 1
    for j in range(2, t_cou - 1):
        if t_cou % j == 0:
            flag = 0
            break
    if flag:
        pna.append(t_cou)
if use_block:  # для блочной формы представления делается перерасчет числа генерируемых символов
    max_len = (1 + (k_len - num_block) // (num_block + 1)) * num_block
    excluded += '-'  # символ "-" добавляется в список исключенных (не генерируется внутри блока)
else:
    max_len = k_len

tmp_list = []
set_order = []
for t_cou in full_list:  # формирование промежуточных списков для "перемешивания" наборов символов
    if t_cou[0] == 1:
        tmp_list.append([t_cou[2], t_cou[1]])
        set_order.append(-1)
for t_cou in range(len(set_order)):  # выбор порядка следования наборов символов (вероятно излишен, но пусть будет)
    if set_order[t_cou] < 0:
        tmp_rnd = int(random() * len(set_order))
        while tmp_rnd in set_order:
            tmp_rnd = int(random() * len(set_order))
        set_order[t_cou] = tmp_rnd

chr_list = []  # список символов с описанием
chr_string = ''  # строка символов по заданным выше критериям для альтернативного алгоритма создания ключа
for bl_cou in range(len(set_order)):  # сборка базового списка символов
    tmp_chr_set = tmp_list[set_order.index(bl_cou)][0]
    for bl2_cou in tmp_chr_set:
        if bl2_cou not in excluded:
            chr_string += bl2_cou  # только для сравнения с альтернативным генератором (например secrets)
            chr_list.append([bl2_cou, tmp_list[set_order.index(bl_cou)][1], 0])
chr_num = len(chr_list)  # число символов в базовом списке

# сборка ключа
symb_pos = int(random() * chr_num)
avg_uses = 1 / chr_num
b_cou = 0
key_string = ''  # конечная последовательность символов (сам ключ)
for chr_pos_cou in range(max_len):
    set_flag = 0  # сброс признака установки символа
    while set_flag == 0:
        symb_pos += pna[int(random() * len(pna))]
        if symb_pos > chr_num-1:
            symb_pos -= (symb_pos // chr_num) * chr_num
        find_flag = 0
        avg_prob = avg_uses / chr_num
        # поиск символов с "вероятностью" использования менее пороговой
        for tmp_cou in range(chr_num):
            chr_uses = chr_list[tmp_cou][2] / (chr_list[tmp_cou][1]*(1-use_eq_prob) + use_eq_prob)  # коррекция used
            if chr_uses < avg_prob:
                find_flag = 1
                break
        if not find_flag:  # символов не найдено, поднимается ограничение "вероятности" (оставлено на всякий случай)
            avg_prob = (avg_uses + 1) / chr_num
            print('Не найдены подходящие символы! Коррекция avg_prob.')
        symb_prob = chr_list[symb_pos][2] / (chr_list[symb_pos][1]*(1-use_eq_prob) + use_eq_prob)
        if symb_prob < avg_prob:  # если символ применим, то сборка кода
            key_string += chr_list[symb_pos][0]
            chr_list[symb_pos][2] += 1
            avg_uses += 1 / (chr_list[symb_pos][1]*(1-use_eq_prob) + use_eq_prob)
            if use_block:  # если нужна разбивка на блоки
                if b_cou == num_block - 1 and chr_pos_cou < max_len-1:
                    key_string += '-'
                    b_cou = 0
                else:
                    b_cou += 1
            set_flag = 1  # все операции завершены, флаг установки = 1
# ключ сформирован


if not use_file:  # без записи в файл
    if COMMENTS:
        print(f'               Сгенерировано key_gen: {key_string}\t\t({len(key_string)} символов из {k_len})')
        alphabet = string.printable[:-6]
        password = ''.join(secrets.choice(alphabet) for i in range(k_len))
        print(f'Secrets на наборе символов из string: {password}\t({len(password)} символов) набор: {alphabet}')
        psw2 = ''.join(secrets.choice(chr_string) for i in range(k_len))
        print(f'     Secrets на моём наборе символов: {psw2}\t({len(psw2)} символов) набор: {chr_string}')
else:  # запись в файл
    curr_path = str(Path(__file__).resolve().parent)
    if os.path.exists(file_name):  # файл уже есть
        f_size = os.stat(file_name).st_size
        f_i = os.stat(file_name)
        exist_flag = 1
        if overwrite_file:
            f_stat = f'был {f_size} байт, перезаписан'
        else:
            f_stat = f'уже есть {f_size} байт, перезапись запрещена'
    else:  # файла нет
        f_stat = 'создан'
        exist_flag = 0
    if use_infile:
        write_string = infile_prefix + key_string + infile_ending
    else:
        write_string = key_string

    if overwrite_file or not exist_flag:
        my_file = open(file_name, "w", encoding="utf-8")
        my_file.write(write_string)
        my_file.close()
        if COMMENTS:
            print(f'Ключ сохранен в {curr_path}\\> {file_name} ({f_stat})')
            my_file = open(file_name, mode="r", encoding="utf-8")  # , encoding="utf-8")
            print('    Base key (new):', key_string)
            print('Прочитано из файла:', my_file.read())
            my_file.close()
    else:
        if COMMENTS:
            print(f'Файл {f_stat}.')
if COMMENTS:
    my_file = open(file_name, mode="r", encoding="utf-8")  # , encoding="utf-8")
    print('    Base key (new):', key_string)
    print('Прочитано из файла:', my_file.read())
    my_file.close()


if COMMENTS:
    print(' -' * 5, 'End output', '- ' * 80)
