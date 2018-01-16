#-*- coding: utf-8 -*-
import psycopg2
from flask import g, request, jsonify
from ..api_1_0 import api
from ..main import main

db_name = "university_db"


# Соединяет с указанной базой данных
def connect_db():
    conn = psycopg2.connect(database=db_name, user="admin", password="admin",
                            host="localhost", port="5432")
    return conn


# Если нет соединения с базой данных, то открыть новое для текущего контекста
@main.before_request
def get_db():
    conn = getattr(g, 'conn_db', None)
    if conn is None:
        conn = g.conn_db = connect_db()
    g.cur_db = conn.cursor()


# Закрыть подключение к БД по завершению запроса
@main.teardown_request
def close_db(response):
    conn = getattr(g, 'conn_db', None)
    if conn is not None:
        conn.close()
    del g.conn_db
    del g.cur_db


# Если нет соединения с базой данных, то открыть новое для текущего контекста
@api.before_request
def get_db():
    conn = getattr(g, 'conn_db', None)
    if conn is None:
        conn = g.conn_db = connect_db()
    g.cur_db = conn.cursor()


# Закрыть подключение к БД по завершению запроса
@api.teardown_request
def close_db(response):
    conn = getattr(g, 'conn_db', None)
    if conn is not None:
        conn.close()
    del g.conn_db
    del g.cur_db


table_names = {'spec': 'specialties', 'disc': 'disciplines',
               'stud': 'students', 'mark': 'marks'}
column_names = {table_names['spec']: ('specialty_id', 'specialty', 'faculty'),
                table_names['disc']: ('discipline_id', 'discipline_name',
                                      'faculty', 'specialty', 'exam_form'),
                table_names['stud']: ('stud_id', 'surname', 'name', 'patronymic',
                                      'group_no', 'faculty', 'specialty'),
                table_names['mark']: ('mark_id', 'mark', 'stud_id',
                                      'discipline_id')}


# GET something
def get_smth_by_string(string):
    g.cur_db.execute(string)
    rows = g.cur_db.fetchall()
    return rows


# GET length
@api.route('/get_smth_length', methods=['POST'])
def get_smth_length():
    table_name = request.json['table_name']
    string = "SELECT COUNT(*) FROM {} ".format(table_name)
    try:
        filters = request.json['filters']
        where_part = "WHERE "
        for i in filters:
            where_part += "{}='{}' AND ".format(i, filters[i])
        if where_part != 'WHERE ':
            string += where_part[:-4]
    except (KeyError, TypeError):
        pass
    g.cur_db.execute(string)
    rows = g.cur_db.fetchall()
    print(rows)
    return jsonify(rows[0][0])


# Get marks count
@api.route('/get_marks_count', methods=['POST'])
def get_marks_count():
    filters = request.json['filters']
    if 'discipline' not in filters:
        string = "SELECT COUNT(*) FROM marks " \
                 "INNER JOIN students ON marks.stud_id = students.stud_id "
        where_part = 'WHERE '
        for i in filters:
            where_part += "{}='{}' AND ".format('students.' + i, filters[i])
    else:
        string = "SELECT COUNT(*) FROM marks " \
                 "INNER JOIN students ON marks.stud_id = students.stud_id " \
                 "INNER JOIN disciplines ON marks.discipline_id = " \
                 "disciplines.discipline_id "
        where_part = 'WHERE '
        for i in filters:
            if i != 'discipline':
                where_part += "{}='{}' AND ".format('students.' + i, filters[i])
            else:
                where_part += "{}='{}' AND "\
                              .format('disciplines.discipline_name', filters[i])
    if where_part != 'WHERE ':
        string += where_part[:-4]
    g.cur_db.execute(string)
    rows = g.cur_db.fetchall()
    return jsonify(rows[0][0])


# GET list of values in one db coloumn
def get_tuple_one_coloumn_values(coloumn_mane, table):
    g.cur_db.execute("SELECT DISTINCT {} from {} ORDER BY {};"
                     .format(coloumn_mane, table, coloumn_mane))
    values = (x[0] for x in g.cur_db.fetchall())
    return values


# Check. Faculty and specialty are exist.
def fac_spec_is_exist(faculty, specialty):
    g.cur_db.execute("SELECT {0} from {1} WHERE {0}='{2}' AND {3}='{4}';".
                     format(column_names[table_names['spec']][2],
                            table_names['spec'], faculty,
                            column_names[table_names['spec']][1], specialty))
    rows = g.cur_db.fetchall()
    if rows:
        return True
    else:
        return False


def add_smth_to_db(table, coloumns_name_list, coloumn_values_list):
    g.cur_db.execute("INSERT INTO {} ({}) VALUES ({});".format(table,
                     ", ".join(coloumns_name_list), ', '.join(["'" + x + "'"
                               for x in coloumn_values_list])))
    g.conn_db.commit()


def update_smth_in_db(table, coloumns_name_list, condition_name,
                      coloumn_values_and_condition_list):
    g.cur_db.execute("UPDATE {} SET  ({}) = ({})  WHERE {} = {};"
                     .format(table, ", ".join(coloumns_name_list),
                     ", ".join(["'" + x + "'" for x in
                                coloumn_values_and_condition_list[:-1]]),
                     condition_name, coloumn_values_and_condition_list[-1]))
    print("UPDATE {} SET  ({}) = ({})  WHERE {} = {};"
          .format(table, ", ".join(coloumns_name_list),
          ", ".join(["'" + x + "'" for x in
                     coloumn_values_and_condition_list[:-1]]),
          condition_name, coloumn_values_and_condition_list[-1]))
    g.conn_db.commit()
    g.conn_db.close()


def delete_smth_in_db(table, condition_name, condition_value):
    g.cur_db.execute("DELETE FROM {} WHERE {} = {};".format(table,
                     condition_name, condition_value))
    g.conn_db.commit()
    g.conn_db.close()


# Check. Discipline is exist on specialty
def is_discipline_exist_on_specialty(specialty, add_discipline):
    g.cur_db.execute("SELECT discipline_name FROM {} WHERE discipline_name="
                     "'{}' AND specialty='{}';".format(table_names['disc'],
                     add_discipline, specialty))
    rows = g.cur_db.fetchall()
    if rows:
        return True
    else:
        return False
