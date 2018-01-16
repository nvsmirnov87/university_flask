#-*- coding: utf-8 -*-
from flask import session, json
from ..main.models import Disciplines, Specialties, Students, Marks
import requests

index_buttons = {Students.table_name['students']: '/students',
                 Specialties.table_name['specialties']: '/specialties',
                 Disciplines.table_name['disciplines']: '/disciplines',
                 Marks.table_name['marks']: '/marks'}


specialties_column_headers = ("№", "Специальность", "Факультет",
                              "Редактирование", "Удаление")
disciplines_column_headers = ("№", "Дисциплина", "Факультет", "Специальность",
                              "Форма аттестации", "Редактирование", "Удаление")
students_column_headers = ("№ студентческого билета", "Фамилия", "Имя",
                           "Отчество", "№ группы", "Факультет", "Специальность",
                           "Профиль", "Редактирование", "Удаление")
marks_column_headers = ("id оценки", 'Оценка', "id дисциплины",
                        'Название дисциплины', "id студента", 'Фамилия', 'Имя',
                        'Отчество', '№ группы', "Редактирование", "Удаление")
profile_column_headers = {'Название дисциплины', 'Оценка'}

marks_mas = ['Не зачтено', 'Зачтено', 'Не аттест.', 'Не удовл.', 'Удовл.',
             'Хорошо', 'Отлично']
exam_form_mas = ('Зачет', 'Экзамен')

LINES_PER_PAGE = 50
curent_api_part = 'http://localhost:5000/api/v1.0/'


def clean_session(*current_session):
    for i in ['filters_disc', 'filters_mark', 'filters_stud', 'filters_spec',
              'table_name_disc', 'table_name_mark', 'table_name_stud',
              'table_name_spec']:
        if i not in current_session:
            try:
                del session[i]
            except:
                pass


# Функция для получения номера отображаемой страницы и соседних страниц
def paginate_func(table_name, filters, page, count_neighbor):
    if table_name != 'marks':
        if len(filters) > 0:
            r_dict = {'table_name': table_name, 'filters': filters}
        else:
            r_dict = {'table_name': table_name}
        req = requests.post(curent_api_part + 'get_smth_length', json=r_dict)
    else:
        req = requests.post(curent_api_part + 'get_marks_count',
                            json={'filters': filters})
    len_parse_list = json.loads(req.text)
    # Get page numbers for <a href=...>
    if float(len_parse_list)/ LINES_PER_PAGE == len_parse_list / LINES_PER_PAGE:
        len_parse_list /= LINES_PER_PAGE
    else:
        len_parse_list = int(len_parse_list / LINES_PER_PAGE) + 1

    list_of_pages = [1]
    # put '...' if it need
    if page > 2 + count_neighbor:
        list_of_pages.append('...')

    # Получаем номера страниц сосоедей слева
    count_neighbor_l = count_neighbor * (-1)
    while count_neighbor_l < 0:
        if page + count_neighbor_l > 1:
            list_of_pages.append(page + count_neighbor_l)
        count_neighbor_l += 1

    # Добавляем в список номера этих страниц
    if page > 1:
        list_of_pages.append(page)

    # Получаем номера страниц сосоедей справа
    plus_neighbor = 1
    while plus_neighbor <= count_neighbor:
        if page + plus_neighbor <= len_parse_list:
            list_of_pages.append(page + plus_neighbor)
        plus_neighbor += 1
    if len_parse_list > page + count_neighbor:
        if len_parse_list > page + count_neighbor + 1:
            list_of_pages.append('...')
        list_of_pages.append(len_parse_list)

    return list_of_pages
