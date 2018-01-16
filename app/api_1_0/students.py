#-*- coding: utf-8 -*-
from flask import jsonify, json, request
from database import table_names, column_names, get_smth_by_string, \
                     add_smth_to_db, update_smth_in_db, delete_smth_in_db
from . import api
from ..main.models import Students
from flask_api import status
from ..static.project_const_and_func import LINES_PER_PAGE


# Получить информацию о студентах
@api.route('/students', methods=["GET", "POST"])
def get_students():
    stud = column_names[table_names['stud']]
    select_string = "SELECT {} FROM {} ".format(', '.join(x for x in stud),
                                                table_names['stud'])

    where_part = "WHERE "
    try:
        filters_dict = request.json['filters']
        for i in filters_dict.keys():
            if i in filters_dict:
                where_part += "{}='{}' AND ".format(i, filters_dict[i])
        if where_part != "WHERE ":
            select_string += where_part[:-4]
    except (TypeError, KeyError):
        pass

    select_string += " ORDER BY {} ".format(stud[0])
    try:
        page = request.json['page']
        select_string += "{} {} ".format('OFFSET', (page - 1) * LINES_PER_PAGE)
        select_string += "{} {} ".format('LIMIT', LINES_PER_PAGE)
    except (TypeError, KeyError):
        pass

    content = jsonify(get_smth_by_string(select_string))
    return content


# Добавить студента
@api.route('/student_add', methods=["POST"])
def add_student():
    stud = column_names[table_names['stud']][1:]
    stud_dict = {}
    for i in range(len(stud)):
        stud_dict.update({stud[i]: request.json[stud[i]]})
    # Проверяем, что заданы корректные данные и добавляем студента в БД
    try:
        if stud_dict[stud[4]] in (u'Факультет не выбран', u'None', u'') or \
           stud_dict[stud[5]] in [u'Факультет не выбран', u'Не выбрано',
                                  u'None', u''] or \
           stud_dict[stud[0]] in [u'None', u''] or \
           stud_dict[stud[1]] in [u'None', u''] or \
           stud_dict[stud[2]] in [u'None', u''] or \
           stud_dict[stud[3]] in [u'None', u'']:
            message = Students.answer['add'][0]
            return jsonify({'Message': message}), status.HTTP_400_BAD_REQUEST
        else:
            try:
                add_smth_to_db(table_names['stud'], (stud[:]),
                               (stud_dict[stud[0]], stud_dict[stud[1]],
                                stud_dict[stud[2]], stud_dict[stud[3]],
                                stud_dict[stud[4]], stud_dict[stud[5]]))
                message = Students.answer['add'][1]
                return(jsonify({'Message': message}), status.HTTP_201_CREATED)
            except:
                message = {'Message': Students.answer['add'][0]}
                return jsonify(message), status.HTTP_400_BAD_REQUEST
    except:
        message = Students.answer['add'][0]
        return jsonify({'Message': message}), status.HTTP_400_BAD_REQUEST


# Отредактировать информацию о студенте
@api.route('/student_edit', methods=["PUT"])
def edit_student():
    stud = column_names[table_names['stud']]
    stud_dict = {x: '' for x in stud[0:5]}
    for i in range(len(stud_dict)):
        stud_dict[stud[i]] = request.json[stud[i]]

    update_smth_in_db(table_names['stud'], stud[1: 5], stud[0],
                      [stud_dict['surname'], stud_dict['name'],
                       stud_dict['patronymic'], stud_dict['group_no'],
                       stud_dict['stud_id']])

    message = {'Message': Students.answer['edit'].format(stud_dict['stud_id'])}
    return jsonify(message)


# Удалить инфомрацию о студенте
@api.route('/student_del', methods=['DELETE'])
def del_student():
    stud_id = column_names[table_names['stud']][0]
    del_id = request.json[stud_id]
    delete_smth_in_db(table_names['stud'], stud_id, del_id)
    content = {'Message': Students.answer['del'].format(del_id)}
    return jsonify(content)


# Получить номера групп на специальности/факультете
@api.route('/group', methods=['POST'])
def get_group_by_facul_spec(*facul_spec):
    stud = column_names[table_names['stud']]
    stud_dict = {x: '' for x in stud[5:]}
    if facul_spec == ():
        for i in range(len(stud_dict)):
            stud_dict[stud[i]] = request.json[stud[i]]
    else:
        student_info = facul_spec[0].get_data()
        student_info = json.loads(student_info)
        for i in range(len(stud_dict)):
            stud_dict[stud[i+5]] = student_info[stud[i+5]]

    select_string = "Select DISTINCT {} FROM {} ".format(stud[4],
                                                         table_names['stud'])
    for key, value in stud_dict.items():
        if value is not None:
            if 'AND ' != select_string[-4:]:
                select_string += " WHERE "
            select_string += "{}='{}' AND ".format(key, value)
    if 'AND ' == select_string[-4:]:
        select_string = select_string[:-4]
    select_string += " ORDER BY {}".format(stud[4])
    coontent = jsonify(get_smth_by_string(select_string))
    return coontent, status.HTTP_200_OK


# Получить студентов в кокретной группе
@api.route('/students_by_group', methods=["POST"])
def get_students_by_group(*group_no):
    where_part = []
    # Обрабатываем request json
    if group_no == ():
        where_part.append((column_names[table_names['stud']][4],
                           request.json[column_names[table_names['stud']][4]]))
    # Обрабатываем вызов из представления
    else:
        group_no = group_no[0].get_data()
        group_no = json.loads(group_no)
        where_part.append((group_no.keys()[0], group_no.values()[0]))
    stud = column_names[table_names['stud']]
    select_string = "SELECT {0} FROM {1} WHERE {3}='{2}' ORDER BY {4};".\
                    format(', '.join(stud[0:4]),
                    table_names['stud'], group_no.values()[0].encode('utf-8'),
                    group_no.keys()[0],
                    ', '.join(column_names[table_names['stud']][1:4]),
                    ', '.join(stud[1:4]))
    content = jsonify(get_smth_by_string(select_string))
    return content, status.HTTP_200_OK


# Получить оценки студента
@api.route('/student_marks', methods=['POST'])
def get_student_marks():
    stud_id = request.json[column_names[table_names['stud']][0]]
    select_strinfg = "SELECT disciplines.discipline_name, marks.mark FROM " \
                     "marks INNER JOIN disciplines ON marks.discipline_id = " \
                     "disciplines.discipline_id WHERE marks.stud_id = {}"\
                     .format(stud_id)
    content = jsonify(get_smth_by_string(select_strinfg))
    return content
