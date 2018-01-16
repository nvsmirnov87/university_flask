#-*- coding: utf-8 -*-
from flask import jsonify, json, request
from database import table_names, column_names, get_smth_by_string, \
                     add_smth_to_db, update_smth_in_db, delete_smth_in_db
from . import api
from ..main.models import Marks
from flask_api import status
from ..static.project_const_and_func import LINES_PER_PAGE, marks_mas, \
                                            exam_form_mas


@api.route('/marks', methods=['GET', 'POST'])
def get_marks():
    mark = column_names[table_names['mark']]
    # Создание строки запроса к БД
    select_string = "SELECT {0}.mark_id, {0}.mark, {1}.discipline_id, " \
                    "{1}.discipline_name, {2}.stud_id, {2}.surname, {2}.name,"\
                    " {2}.patronymic, {2}.group_no FROM {0} INNER JOIN {2} " \
                    "ON {0}.stud_id = {2}.stud_id INNER JOIN {1} ON " \
                    "{0}.discipline_id = {1}.discipline_id "\
                    .format('marks', 'disciplines', 'students')
    # Добавление условия (WHERE)
    where_part = "WHERE "
    try:
        filters_dict = request.json['filters']
        for i in filters_dict.keys():
            if i != 'discipline':
                where_part += "{}='{}' AND ".format('students.' + i,
                                                    filters_dict[i])
            else:
                where_part += "{}='{}' AND "\
                    .format('disciplines.discipline_name', filters_dict[i])
        if where_part != "WHERE ":
            select_string += where_part[:-4]
    except (KeyError, TypeError):
        pass
    # Добавление сортировки (ORDER BY) и ограничений (OFFSET, LIMIT)
    select_string += " ORDER BY {} ".format(mark[0])
    try:
        page = request.json['page']
        select_string += "{} {} ".format('OFFSET', (page - 1) * LINES_PER_PAGE)
        select_string += "{} {} ".format('LIMIT', LINES_PER_PAGE)
    except (KeyError, TypeError):
        pass
    content = jsonify(get_smth_by_string(select_string))
    return content


# Получение формы аттестации (Экзамен/Зачет) по дисциплине
@api.route('/get_exam_form', methods=['POST'])
def get_exam_form():
    disc = column_names[table_names['disc']]
    disc_id = request.json[disc[0]]
    string = "SELECT {} FROM {} WHERE {}='{}'"\
        .format(disc[4], table_names['disc'], disc[0], disc_id)
    return jsonify(get_smth_by_string(string))


# Добавление новой оценки
@api.route('/mark_add', methods=["POST"])
def add_mark():
    mark = column_names[table_names['mark']][1:]
    mark_dict = {}
    for i in range(len(mark)):
        mark_dict.update({mark[i]: request.json[mark[i]]})
    # Проверяем, что этот студент изучет указанную дисциплину
    t_stud = table_names['stud']
    t_disc = table_names['disc']
    stud_id = t_stud + '.' + column_names[table_names['stud']][0]
    discipline_id = t_disc + '.' + column_names[table_names['disc']][0]
    string = "SELECT {0} FROM {1} INNER JOIN {2} ON {1}.faculty={2}.faculty " \
             "AND {1}.specialty = {2}.specialty WHERE {0}={3} AND {4}={5}"\
             .format(stud_id, t_stud, t_disc, int(mark_dict['stud_id']),
             discipline_id, int(mark_dict['discipline_id']))
    result = get_smth_by_string(string)
    if result == []:
        content = "Введены некорректные данные. " \
                  "Студент id={} не изучает дисциплину id={}".\
                  format(mark_dict['stud_id'], mark_dict['discipline_id'])
        return jsonify(content), status.HTTP_400_BAD_REQUEST
    else:
        # Проверим, что введена корректная оценка
        string = "SELECT {} FROM {} WHERE {}={}"\
                 .format(column_names[t_disc][4],
                 t_disc, column_names[t_disc][0], mark_dict['discipline_id'])
        exam_form = get_smth_by_string(string)[0][0]
        if exam_form == exam_form_mas[0] and mark_dict['mark'] in marks_mas[2:] or \
           exam_form == exam_form_mas[1] and mark_dict['mark'] in marks_mas[:2]:
            content = "Введены некорректные данные. Введенная оценка '{}' " \
                      "не соотвествует форме аттестации дисциплины id={}". \
                      format(mark_dict['mark'], mark_dict['discipline_id'])
            return jsonify(content), status.HTTP_400_BAD_REQUEST
        else:
            add_smth_to_db(table_names['mark'], mark_dict.keys(),
                           mark_dict.values())
            content = Marks.answer['add'][0]
            return jsonify(content), status.HTTP_201_CREATED


# Редактирование оценки
@api.route('/mark_edit', methods=["PUT"])
def edit_mark():
    mark = column_names[table_names['mark']][:2]
    mark_dict = {x: '' for x in mark}
    for i in range(len(mark_dict)):
        mark_dict[mark[i]] = request.json[mark[i]]
    coloumn_values_and_condition_list = [mark_dict[mark[1]],
                                         mark_dict[mark[0]]]
    update_smth_in_db(table_names['mark'], (mark[1],), mark[0],
                      coloumn_values_and_condition_list)
    message = Marks.answer['edit'].format(mark_dict[mark[0]])
    return jsonify({'Message':message})


# Удаление оценки
@api.route('/mark_del', methods=['DELETE'])
def del_mark():
    mark = column_names[table_names['mark']][0]
    del_id = request.json[mark]
    delete_smth_in_db(table_names['mark'], mark, del_id)
    content = Marks.answer['del'].format(del_id)
    return jsonify({'Message': content})
