#-*- coding: utf-8 -*-
from flask import jsonify, json, request

from database import table_names, column_names, get_smth_by_string, \
                     add_smth_to_db, fac_spec_is_exist, \
                     update_smth_in_db, delete_smth_in_db
from . import api
from ..main.models import Specialties
from flask_api import status
from ..static.project_const_and_func import LINES_PER_PAGE

# Получние специальностей
@api.route('/specialties', methods=['GET', 'POST'])
def specialties():
    # Создание сроки запроса к БД
    spec = column_names[table_names['spec']]
    select_string = "SELECT {} FROM {} ".format(', '.join((x for x in spec)),
                                                table_names['spec'])

    # Добавление в строку зароса условия (WHERE)
    try:
        filters_dict = request.json['filters']
        if spec[2] in filters_dict:
            select_string += "WHERE {}='{}' ".format(spec[2],
                                                     filters_dict[spec[2]])
    # Исключение для GET и POST запросов соотвественно
    except (TypeError, KeyError) :
        pass
    # Добавление сортировки (ORDER BY) и ограничений (OFFSET, LIMIT)
    select_string += " ORDER BY {} ".format(spec[1])
    try:
        page = request.json['page']
        select_string += "{} {} ".format('OFFSET', (page-1) * LINES_PER_PAGE)
        select_string += "{} {} ".format('LIMIT', LINES_PER_PAGE)
    # Исключение для GET и POST запросов соотвественно
    except (TypeError, KeyError):
        pass
    content = jsonify(get_smth_by_string(select_string))
    return content


# Получние название специальностей для формы
@api.route('/form_specialties', methods=['GET', 'POST'])
def form_specialties():
    spec = column_names[table_names['spec']]
    select_string = "SELECT {} FROM {} ".format(spec[1], table_names['spec'])
    faculty = request.form['f_faculty']
    select_string += "WHERE {}='{}' ".format(spec[2], faculty)
    select_string += " ORDER BY {} ".format(spec[1])
    content = json.dumps(get_smth_by_string(select_string))
    return content


# Добавление специальнсотей
@api.route('/specialty_add', methods=['POST'])
def add_speciaty():
    spec = column_names[table_names['spec']]
    specialty = request.json[spec[1]]
    faculty = request.json[spec[2]]
    # Проверяем есть ли такая специальность на факультете.
    # Если нет, то добавляем специальность на факультет
    if fac_spec_is_exist(faculty, specialty):
        content = jsonify({'Message': Specialties.answer['add'][0].
                           format(specialty, faculty)})
        return content, status.HTTP_400_BAD_REQUEST
    else:
        add_smth_to_db(table_names['spec'], spec[1:], (specialty, faculty))
        content = jsonify({'Message': Specialties.answer['add'][1].
                          format(specialty, faculty)})
        return content, status.HTTP_201_CREATED


# Редактирвоание информации о специальности
@api.route('/specialty_edit', methods=['PUT'])
def edit_specialty():
    spec = column_names[table_names['spec']]
    # Проверяем зашли ли мы с views или зашли из стороннего ресурса
    spec_dict = {x: '' for x in spec}
    for i in range(len(spec_dict)):
        spec_dict[spec[i]] = request.json[spec[i]]
    spec_dict.update({"new_specialty_name":
                      request.json["new_specialty_name"]})

    if spec_dict['specialty'] == spec_dict['new_specialty_name']:
        content = jsonify({'Message': Specialties.answer['edit'][1].
                          format(spec_dict['specialty'])})
        return content, status.HTTP_400_BAD_REQUEST
    elif fac_spec_is_exist(spec_dict['faculty'],
                           spec_dict['new_specialty_name']):
        content = jsonify({'Message': Specialties.answer['edit'][0].
                           format(spec_dict['new_specialty_name'],
                           spec_dict['faculty'])})
        return content, status.HTTP_400_BAD_REQUEST
    else:
        update_smth_in_db(table_names['spec'], (spec[1],), spec[0],
                          (spec_dict['new_specialty_name'],
                           spec_dict['specialty_id']))
        content = jsonify({'Message': Specialties.answer['edit'][2].
                          format(spec_dict['specialty'],
                                 spec_dict['faculty'])})
        return content


# Удаляем специальность
@api.route('/specialty_del', methods=['DELETE'])
def del_speciaty():
    spec_id = column_names[table_names['spec']][0]
    del_id = request.json[spec_id]
    delete_smth_in_db(table_names['spec'], spec_id, del_id)
    content = jsonify({'Message': Specialties.answer['del'].format(del_id)})
    return content
