#-*- coding:utf-8 -*-
from flask import jsonify
from . import api
from database import table_names, column_names, get_tuple_one_coloumn_values


# Получение списка всех факультетов + записи "Все факультеты"
@api.route('/faculties_ext', methods=['GET'])
def faculties_ext():
    choices = ["Все факультеты"]
    choices.extend([i for i in get_tuple_one_coloumn_values(column_names
                    [table_names['spec']][2], table_names['spec'])])
    return jsonify(choices)


# Получение списка всех факультетов
@api.route('/faculties', methods=['GET'])
def faculties():
    choices = ([i for i in get_tuple_one_coloumn_values(column_names
                [table_names['spec']][2], table_names['spec'])])
    return jsonify(choices)
