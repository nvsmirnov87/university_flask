#-*- coding: utf-8 -*-
from flask import jsonify, request
from database import table_names, column_names, get_smth_by_string, \
                     add_smth_to_db, is_discipline_exist_on_specialty, \
                     update_smth_in_db, delete_smth_in_db
from . import api
from ..main.models import Disciplines
from flask_api import status
from ..static.project_const_and_func import LINES_PER_PAGE


# Получаем дисциплипны
@api.route('/disciplines', methods=["GET", "POST"])
def get_disciplines():
    spec = column_names[table_names['spec']]
    disc = column_names[table_names['disc']]

    # Создаем строку запроса к БД
    select_string = "SELECT {} FROM {} ".format((', ').join(x for x in disc),
                                                table_names['disc'])

    # К строке зарпоса доабвляем условие (WHERE)
    where_part = "WHERE "
    try:
        filters_dict = request.json['filters']
        for i in [spec[1], spec[2]]:
            if i in filters_dict:
                where_part += "{}='{}' AND ".format(i, filters_dict[i])
        if where_part != "WHERE ":
            select_string += where_part[:-4]
    # Исключение для GET и POST запросов соотвественно
    except (TypeError, KeyError):
        pass
    # Добавляем сортировку (ORDER BY) и ограничения (OFFSET, LIMIT)
    select_string += " ORDER BY {} ".format(disc[0])
    try:
        page = request.json['page']
        select_string += "{} {} ".format('OFFSET', (page-1)*LINES_PER_PAGE)
        select_string += "{} {} ".format('LIMIT', LINES_PER_PAGE)
    except (TypeError, KeyError):
        pass

    coontent = jsonify(get_smth_by_string(select_string))
    return coontent


# Добавляем новую дисциплину
@api.route('/discipline_add', methods=["POST"])
def add_discipline():
    disc = column_names[table_names['disc']]
    # обработка request json запроса
    discipline_info = ({disc[1]: request.json[disc[1]],
                        disc[2]: request.json[disc[2]],
                        disc[3]: request.json[disc[3]],
                        disc[4]: request.json[disc[4]]})

    if is_discipline_exist_on_specialty(discipline_info[disc[3]],
                                        discipline_info[disc[1]]):
        message = Disciplines.answer['add'][1].\
                  format(discipline_info[disc[1]], discipline_info[disc[3]])
        content = jsonify({'Message':message})
        return content, status.HTTP_400_BAD_REQUEST
    else:
        add_smth_to_db(table_names['disc'], (x for x in column_names[
                       table_names['disc']][1:]), (discipline_info[disc[1]],
                       discipline_info[disc[2]], discipline_info[disc[3]],
                        discipline_info[disc[4]]))
        message = Disciplines.answer['add'][2].format(discipline_info[disc[1]])
        coontent = jsonify({'Message': message})
        return coontent, status.HTTP_200_OK


# Редактируем дисциплину
@api.route('/discipline_edit', methods=["PUT"])
def edit_discipline():
    disc = column_names[table_names['disc']]
    specialty = request.json[disc[3]]
    discipline_new_name = request.json['discipline_new_name']
    examination_form = request.json[disc[4]]
    discipline_id = request.json[disc[0]]

    if is_discipline_exist_on_specialty(specialty, discipline_new_name):
        message = Disciplines.answer['edit'][0].format(discipline_new_name,
                                                       specialty)
        return jsonify({'Message':message}), status.HTTP_400_BAD_REQUEST
    else:
        update_smth_in_db(table_names['disc'], [disc[1], disc[4]],
                          disc[0], [discipline_new_name, examination_form,
                                    discipline_id])
        message = {'Message': Disciplines.answer['edit'][1].
                   format(discipline_id)}
        return jsonify(message)


# Удаляем дисциплину
@api.route('/discipline_del', methods=['DELETE'])
def del_discipline():
    disc = column_names[table_names['disc']]
    del_id = request.json[disc[0]]
    delete_smth_in_db(table_names['disc'], disc[0], del_id)
    content = {'Message': Disciplines.answer['del'].format(del_id)}
    return jsonify(content)
