from django import template

register = template.Library()

# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.

# Пример:
# @register.filter()  # Декоратор register.filter() указывает Django, что нужно запомнить про существование нового
# фильтра. Название фильтра по умолчанию берется равным названию функции, то есть в шаблонах мы можем писать
# {{ price|currency }}. Однако Django дает нам возможность самим указать название фильтра. Например, если бы мы указали
# register.filter(name=’currency_rub’), а название функции не меняли, тогда в шаблонах мы вызывали фильтр следующим
# образом {{ price|currency_rub }}.
# После добавления файла с новыми фильтрами, необходимо перезагрузить Django-сервер.
# Просто взять и указать функцию в шаблоне не получится. Django лениво работает с фильтрами (бережет оперативную память,
# время и так далее), и для начала нам нужно сказать, что мы хотим подключить свои фильтры. Сделать это можно с помощью
# указания тега {% load custom_filters %}. Где сustom_filters — это название Python файла, который мы создали в папке
# simpleapp/templatetags/.

# def currency(value):
#    """
#    value: значение, к которому нужно применить фильтр
#    """
#    # Возвращаемое функцией значение подставится в шаблон.
#    return f'{value} Р'

# my (old):
# black_list = ['бра*', 'для', 'из*я', '*ать', 'фай*', 'свед*', 'ва*', 'нецен*', '*сказ*', ]
# change_list = ['@#$!', 'for', 'img', '*!', 'file', 'info', 'U!', 'uncensored', '*', ]
#
#
# @register.filter()
# def censor(value):
#     if not isinstance(value, str):
#         raise UserException('Error type')
#     text = value
#     w_type = 1; c_word = ''; txt_list = []
#     for c_symb in text:
#         if w_type == 1:
#             if c_symb.isalpha():
#                 c_word += c_symb
#             else:
#                 txt_list.append(c_word); c_word = c_symb; w_type = 0
#         else:
#             if not c_symb.isalpha():
#                 c_word += c_symb
#             else:
#                 txt_list.append(c_word); c_word = c_symb; w_type = 1
#     txt_list.append(c_word)
#
#     censored_txt = ''  # ; chk_word = ['', 0]
#     for cur_word in txt_list:
#         chk_word = [cur_word.lower(), len(cur_word)]
#         if chk_word[0].isalpha():  # это только текст
#             if chk_word[1] > 2:
#                 cng_flag = 0
#                 for cns_word in black_list:
#                     cw_pars = [cns_word.lower(), len(cns_word), cns_word.find('*')+1]
#                     # if (len(cns_word)>3 and sign(cns_word.find('*')<0) or ....
#                     if cw_pars[2] == 0:  # без пропусков (*)
#                         if chk_word[0] == cw_pars[0]:
#                             cng_flag = 1
#                             var = change_list[black_list.index(cw_pars[0])]
#                             if len(var) < 2:
#                                 censored_txt += var*(chk_word[1])
#                             else:
#                                 censored_txt += var
#                     elif cw_pars[0][0] == '*' and cw_pars[0][-1] == '*':
#                         if cw_pars[0][1:-1] in chk_word[0]:
#                             cng_flag = 1
#                             var = change_list[black_list.index(cw_pars[0])]
#                             if len(var) < 2:
#                                 censored_txt += var * (chk_word[1])
#                             else:
#                                 censored_txt += var
#                     elif cw_pars[2] == cw_pars[1]:  # in the end
#                         if chk_word[0][0:cw_pars[1]-1] == cw_pars[0][0:cw_pars[1]-1]:
#                             cng_flag = 1
#                             var = change_list[black_list.index(cw_pars[0])]
#                             if len(var) < 2:
#                                 censored_txt += var * (chk_word[1])
#                             else:
#                                 censored_txt += var
#                     elif cw_pars[2] == 1:  # in begin
#                         if chk_word[0][-cw_pars[1]+1:chk_word[1]] == cw_pars[0][-cw_pars[1]+1:cw_pars[1]]:
#                             cng_flag = 1
#                             var = change_list[black_list.index(cw_pars[0])]
#                             if len(var) < 2:
#                                 censored_txt += var * (chk_word[1])
#                             else:
#                                 censored_txt += var
#                     elif cw_pars[2] > 1 and (cw_pars[2] < cw_pars[1]):
#                         if chk_word[0][0:cw_pars[2]-1] == cw_pars[0][0:cw_pars[2]-1] and chk_word[0][-(cw_pars[1]-cw_pars[2]):chk_word[1]] == cw_pars[0][-(cw_pars[1]-cw_pars[2]):cw_pars[1]]:
#                             cng_flag = 1
#                             var = change_list[black_list.index(cw_pars[0])]
#                             if len(var) < 2:
#                                 censored_txt += var * (chk_word[1])
#                             else:
#                                 censored_txt += var
#                 if cng_flag == 0:
#                     censored_txt += cur_word
#             else:
#                 censored_txt += cur_word
#         else:
#             censored_txt += cur_word
#     return censored_txt