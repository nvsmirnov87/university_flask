#-*- coding: utf-8 -*-
from flask import render_template, flash, redirect, session, json
from flask_api import status
from . import main
from ..static.project_const_and_func import clean_session, index_buttons, \
    specialties_column_headers, paginate_func, curent_api_part, \
    students_column_headers, marks_column_headers, profile_column_headers, \
    disciplines_column_headers
from forms import FormSelectFaculty, FormAddSpecialty, FormEditSpecialty, \
    FormSelectFacultySpecialty, FormAddDiscipline, FormEditDiscipline, \
    FormSelectStudents, FormAddStudent, FormEditStudent, FormSelectMarks, \
    FormAddMark, FormEditMark
from models import Specialties, Disciplines, Students, Marks
from ..api_1_0.database import table_names as db_table_names, \
    column_names as db_column_names
import requests

# Главное меню
@main.route('/')
@main.route('/index')
def index():
    clean_session([])  # Удаляем сессионные фильтры
    table_name = "Базы данных:"
    return render_template("index.html",
                           table_name=table_name,
                           buttons_first_line=index_buttons
                           )


# Получение информации о специальностях
@main.route('/specialties', methods=['GET', 'POST'])
@main.route('/specialties/page=<int:page>', methods=['GET', 'POST'])
def specialties(page=1):
    # Удаляем лишние сессионные фильтры
    clean_session('filters_spec', 'table_name_spec')
    # Проверяем заданы ли сессионные фильтры, название таблицы и применяем их
    try:
        filters = session['filters_spec']
    except KeyError:
        filters = {}
    try:
        table_name = session['table_name_spec']
    except KeyError:
        table_name = "Специальности "

    facul_label = db_column_names[db_table_names['spec']][2]
    faculty = FormSelectFaculty()
    # Получаем строки таблицы
    if faculty.validate_on_submit():
        filters = {}
        table_name = "Специальности "
        if faculty.f_faculty.data != "Все факультеты":
            table_name += "факультета {}".format(faculty.f_faculty.data)
            filters = {facul_label: faculty.f_faculty.data}
        session['filters_spec'] = filters
        session['table_name_spec'] = table_name
        page = 1
    req = requests.post(curent_api_part + 'specialties',
                        json={'filters': filters, 'page': page})
    show_lines = json.loads(req.text)
    print('len ===', len(show_lines))
    # Получаем номера сраниц
    (link_pages) = paginate_func(table_name=db_table_names['spec'],
                                  filters=filters, page=int(page),
                                  count_neighbor=2)
    link = '/specialties/page='
    return render_template("get_table.html",
                           table_name=table_name,
                           column_headers=specialties_column_headers,
                           show_lines=show_lines,
                           title=Specialties.table_name['specialties'],
                           forms=[faculty],
                           link=link,
                           link_pages=link_pages,
                           buttons=Specialties.buttons
                           )


# Добавление новой специальности
@main.route('/specialty_add', methods=['GET', 'POST'])
def specialty_add():
    clean_session([])  # Удаляем сессионные фильтры
    form_add_specialty = FormAddSpecialty()
    add_specialty = form_add_specialty.s_specialty_name.data
    faculty_of_add_specialty = form_add_specialty.f_faculty.data

    if form_add_specialty.validate_on_submit():
        fac_spec = {db_column_names[db_table_names['spec']][1]: add_specialty,
                    db_column_names[db_table_names['spec']][2]:
                    faculty_of_add_specialty}
        req = requests.post(curent_api_part + 'specialty_add', json=fac_spec)
        message = json.loads(req.text)['Message']
        flash(message)
        return redirect('/specialties')

    return render_template("add_edit_value.html",
                           table_name=Specialties.table_name['specialty_add'],
                           title=Specialties.table_name['specialty_add'],
                           forms=[form_add_specialty]
                           )


# Редактирование специальности
@main.route('/specialty_edit/<edit_faculty>/<edit_spec>/<specialty_id>',
            methods=['GET', 'POST'])
def specialty_edit(specialty_id, edit_faculty, edit_spec):
    spec = db_column_names[db_table_names['spec']]
    form_edit_specialty = FormEditSpecialty()
    new_specialty_name = form_edit_specialty.specialty_name.data

    if form_edit_specialty.validate_on_submit():
        fac_spec_newname_id = {spec[1]: edit_spec, spec[2]: edit_faculty,
                               "new_specialty_name":  new_specialty_name,
                               spec[0]: specialty_id}
        req = requests.put(curent_api_part + 'specialty_edit',
                           json=fac_spec_newname_id)
        message = json.loads(req.text)['Message']
        flash(message)
        return redirect('/specialties')
    table_name = Specialties.table_name['specialty_edit'].format(edit_spec,
                                                                 edit_faculty)
    return render_template("add_edit_value.html",
                           table_name=table_name,
                           title="Редактирование",
                           forms=[form_edit_specialty]
                           )


# Удаление специальности
@main.route('/specialty_del/<specialty_id>', methods=['GET', 'POST'])
def specialty_del(specialty_id):
    del_id = {db_column_names[db_table_names['spec']][0]: specialty_id}
    req = requests.delete(curent_api_part + 'specialty_del', json=del_id)
    message = json.loads(req.text)['Message']
    flash(message)
    return redirect('/specialties')


# получение информации о дисциплинах
@main.route('/disciplines', methods=['GET', 'POST'])
@main.route('/disciplines/page=<int:page>', methods=['GET', 'POST'])
def disciplines(page=1):
    # удаляем лишние сессионные фильтры
    clean_session('filters_disc', 'table_name_disc')
    # проверяем заданы ли сессионные фильтры, название таблицы и применяем их
    try:
        filters = session['filters_disc']
    except KeyError:
        filters = {}
    try:
        table_name = session['table_name_disc']
    except KeyError:
        table_name = "Дисциплины "

    # Получим фильтры и название таблицы
    spec = db_column_names[db_table_names['spec']]
    facul_spec = FormSelectFacultySpecialty()
    if facul_spec.is_submitted():
        filters = {}
        table_name = "Дисциплины "
        if facul_spec.f_faculty.data not in (u'None', u"Факультет не выбран"):
            table_name += "факультета {} ".format(facul_spec.f_faculty.data)
            filters.update({spec[2]: facul_spec.f_faculty.data})
            if facul_spec.s_specialty.data not in (u'None', u"Не выбрано",
                                                   u"Факультет не выбран"):
                filters.update({spec[1]: facul_spec.s_specialty.data})
                table_name += "специальности {}"\
                              .format(facul_spec.s_specialty.data)
        session['filters_disc'] = filters
        session['table_name_disc'] = table_name
        page = 1
    req = requests.post(curent_api_part + 'disciplines',
                        json={'filters': filters, 'page': page})
    show_lines = json.loads(req.text)
    # Получим номера страниц
    (link_pages) = paginate_func(table_name=db_table_names['disc'],
                                  filters=filters, page=int(page),
                                  count_neighbor=2)
    link = '/disciplines/page='

    return render_template("select_faculty_specialty.html",
                           table_name=table_name,
                           column_headers=disciplines_column_headers,
                           show_lines=show_lines,
                           title=Disciplines.table_name['disciplines'],
                           forms=[facul_spec],
                           page=page,
                           link=link,
                           link_pages=link_pages,
                           buttons=Disciplines.buttons)


# Добавление новой дисциплины
@main.route('/discipline_add', methods=['GET', 'POST'])
def discipline_add():
    clean_session([])  # Удаляем сессионные фильтры
    disc = db_column_names[db_table_names['disc']]
    table_name = Disciplines.table_name['discipline_add']
    discipline = FormAddDiscipline()
    if discipline.is_submitted():
        if discipline.f_faculty.data in (u"Факультет не выбран", u'None'):
            flash("Выберите факультет")
            return redirect('/discipline_add')
        elif discipline.s_specialty.data in (u"Не выбрано", u'None'):
            flash("Выберите специальность")
            return redirect('/discipline_add')
        else:
            # Добавляем дисциплину
            disc_dict = {disc[1]: discipline.discipline_name.data,
                         disc[4]: discipline.exam_form.data,
                         disc[2]: discipline.f_faculty.data,
                         disc[3]: discipline.s_specialty.data}
            req = requests.post(curent_api_part + 'discipline_add',
                                json=disc_dict)
            message = json.loads(req.text)['Message']
            flash(message)
            if req.status_code == status.HTTP_400_BAD_REQUEST:
                return redirect('/discipline_add')
            elif req.status_code == status.HTTP_200_OK:
                return redirect('/disciplines')
    return render_template("add_disc_or_stud.html",
                           table_name=table_name,
                           title=table_name,
                           forms=[discipline])


# Редактирование дисциплины
@main.route('/discipline_edit/<discipline_id>/<edit_discipline_name>/' +
            '<specialty>', methods=['GET', 'POST'])
def discipline_edit(discipline_id, edit_discipline_name, specialty):
    table_name = "Редактирование информации о дисциплине " + \
                 edit_discipline_name + ' специальности ' + specialty
    discipline = FormEditDiscipline()

    if discipline.validate_on_submit():
        disc = db_column_names[db_table_names['disc']]
        disc_dict = {disc[0]: discipline_id,
                     disc[3]: specialty,
                     disc[4]: discipline.exam_form.data,
                     'discipline_new_name': discipline.discipline_name.data,
                     }
        req = requests.put(curent_api_part + 'discipline_edit', json=disc_dict)
        message = json.loads(req.text)['Message']
        flash(message)
        return redirect('/disciplines')

    return render_template("add_edit_value.html",
                           table_name=table_name,
                           title="Редактирование",
                           forms=[discipline])


# Удаление дисциплины
@main.route('/discipline_del/<discipline_id>', methods=['GET', 'POST'])
def discipline_del(discipline_id):
    del_id = {db_column_names[db_table_names['disc']][0]: discipline_id}
    req = requests.delete(curent_api_part + 'discipline_del', json=del_id)
    message = json.loads(req.text)['Message']
    flash(message)
    return redirect('/disciplines')


# Получение информации о студентах
@main.route('/students', methods=['GET', 'POST'])
@main.route('/students/page=<int:page>', methods=['GET', 'POST'])
def students(page=1):
    # Удаляем лишние сессионные фильтры
    clean_session('filters_stud', 'table_name_stud')
    # Проверяем заданы ли сессионные фильтры, название таблицы и применяем их
    try:
        filters = session['filters_stud']
    except KeyError:
        filters = {}
    try:
        table_name = session['table_name_stud']
    except KeyError:
        table_name = "Студенты "
    stud = db_column_names[db_table_names['stud']]
    # Проверяем Фильтры:
    student = FormSelectStudents()
    if student.is_submitted():
        filters = {}
        table_name = "Студенты "
        if student.f_faculty.data not in (u'None', u"Факультет не выбран"):
            filters.update({stud[5]: student.f_faculty.data})
            table_name += "факультета {} ".format(student.f_faculty.data)
        if student.s_specialty.data not in (u'None', u"Факультет не выбран",
                                            u'Не выбрано'):
            filters.update({stud[6]: student.s_specialty.data})
            table_name += "специальности {} ".format(student.s_specialty.data)
        if student.g_group.data not in (None, ''):
            filters.update({stud[4]: student.g_group.data})
            table_name += "группы {} ".format(student.g_group.data)
        if student.s_surname.data not in (None, ''):
            filters.update({stud[1]: student.s_surname.data})
            table_name += "{} ".format(student.s_surname.data)
        if student.n_name.data not in (None, ''):
            filters.update({stud[2]: student.n_name.data})
            table_name += "{} ".format(student.n_name.data)
        if student.p_patronymic.data not in (None, ''):
            filters.update({stud[3]: student.p_patronymic.data})
            table_name += "{} ".format(student.p_patronymic.data)
        page = 1
        session['filters_stud'] = filters
        session['table_name_stud'] = table_name
    req = requests.post(curent_api_part + 'students',
                        json={'filters': filters, 'page': page})
    show_lines = json.loads(req.text)
    # Get page numbers for paginate
    (link_pages) = paginate_func(table_name=db_table_names['stud'],
                                  filters=filters, page=int(page),
                                  count_neighbor=2)
    link = '/students/page='
    return render_template("select_faculty_specialty.html",
                           table_name=table_name,
                           column_headers=students_column_headers,
                           show_lines=show_lines,
                           title=Students.table_name['students'],
                           forms=[student],
                           page=page,
                           link=link,
                           link_pages=link_pages,
                           buttons=Students.buttons)


# профилдь студента
@main.route('/student_profile/<stud_id>/<surname>/<name>/<patronymic>/' +
            '<group_no>/<faculty>/<specialty>', methods=['GET', 'POST'])
def student_profile(stud_id, surname, name, patronymic, group_no,
                    faculty, specialty):
    req = requests.post(curent_api_part + 'student_marks',
                        json={db_column_names[db_table_names['stud']][0]:
                              stud_id})
    show_lines = json.loads(req.text)
    return render_template("profile.html",
                           top=(("Номер студентческого билета ", stud_id),
                                ("ФИО", " ".join([surname, name, patronymic])),
                                ("Группа ", group_no),
                                ("Факультет ", faculty),
                                ("Специальность ", specialty)),
                           column_headers=profile_column_headers,
                           show_lines=show_lines,
                           title="Профиль студента",
                           buttons=Students.buttons)


# Добавление нового студента
@main.route('/student_add', methods=['GET', 'POST'])
def student_add():
    clean_session([])  # Удаляем сессионные фильтры
    stud = db_column_names[db_table_names['stud']]
    # Фильтры:
    add_student = FormAddStudent()
    if add_student.is_submitted():
        stud_dict = {stud[1]: add_student.s_surname.data,
                     stud[2]: add_student.n_name.data,
                     stud[3]: add_student.p_patronymic.data,
                     stud[4]: add_student.g_group.data,
                     stud[5]: add_student.f_faculty.data,
                     stud[6]: add_student.s_specialty.data}
        req = requests.post(curent_api_part + 'student_add', json=stud_dict)
        message = json.loads(req.text)['Message']
        flash(message)
        if req.status_code == status.HTTP_201_CREATED:
            return redirect('/students')
        else:
            return redirect('/student_add')

    return render_template("add_disc_or_stud.html",
                           table_name=Students.table_name['student_add'],
                           title=Students.table_name['student_add'],
                           forms=[add_student])


# Редактирование информации о студенте
@main.route('/student_edit/<stud_id>/<surname>/<name>/<patronymic>/<group_no>',
            methods=['GET', 'POST'])
def student_edit(stud_id, surname, name, patronymic, group_no):
    table_name = "Редактирование информации о студенте " + surname + ' ' +\
                 name + ' ' + patronymic + ' из группы № ' + group_no
    edit_student = FormEditStudent()
    if edit_student.validate_on_submit():
        stud = db_column_names[db_table_names['stud']]
        stud_dict = {stud[0]: stud_id,
                     stud[1]: edit_student.s_surname.data,
                     stud[2]: edit_student.n_name.data,
                     stud[3]: edit_student.p_patronymic.data,
                     stud[4]: edit_student.g_group.data}
        req = requests.put(curent_api_part + 'student_edit', json=stud_dict)
        message = json.loads(req.text)['Message']
        flash(message)
        return redirect('/students')

    return render_template("add_edit_value.html",
                           table_name=table_name,
                           title="Редактирование",
                           forms=[edit_student])


# Удаление инфлорации о студенте
@main.route('/student_del/<stud_id>', methods=['GET', 'POST'])
def student_del(stud_id):
    del_id = {db_column_names[db_table_names['stud']][0]: stud_id}
    req = requests.delete(curent_api_part + 'student_del', json=del_id)
    message = json.loads(req.text)['Message']
    flash(message)
    return redirect('/students')


# Получение информации об оценках
@main.route('/marks', methods=['GET', 'POST'])
@main.route('/marks/page=<int:page>', methods=['GET', 'POST'])
def marks(page=1):
    # Удаляем лишние сессионные фильтры
    clean_session('filters_mark', 'table_name_mark')
    # Проверяем заданы ли сессионные фильтры, название таблицы и применяем их
    try:
        filters = session['filters_mark']
    except KeyError:
        filters = {}
    try:
        table_name = session['table_name_mark']
    except KeyError:
        table_name = "Оценки "
    stud = db_column_names[db_table_names['stud']]
    # Фильтры:
    filters_form = FormSelectMarks()
    # Автоматическая фильтрация по факультету
    if filters_form.f_faculty.data == u'None' and stud[5] not in filters:
        filters = {stud[5]: filters_form.f_faculty.default}
        table_name = "Оценки факультета {} ".format(filters[stud[5]])
    # Проверяем изменились ли другие фильтры
    if filters_form.is_submitted():
        filters = {}
        if filters_form.f_faculty.data != u'None':
            filters[stud[5]] = filters_form.f_faculty.data
            table_name = "Оценки факультета {} ".format(filters[stud[5]])
        if filters_form.s_specialty.data not in (u'None', u'', u'Не выбрано'):
            filters.update({stud[6]: filters_form.s_specialty.data})
            table_name += "специальности {} "\
                          .format(filters_form.s_specialty.data)
        if filters_form.g_group.data not in (None, ''):
            filters.update({stud[4]: filters_form.g_group.data})
            table_name += "группы {} ".format(filters_form.g_group.data)
        if filters_form.s_surname.data not in (None, ''):
            filters.update({stud[1]: filters_form.s_surname.data})
            table_name += "{} ". format(filters_form.s_surname.data)
        if filters_form.n_name.data not in (None, ''):
            filters.update({stud[2]: filters_form.n_name.data})
            table_name += "{} ".format(filters_form.n_name.data)
        if filters_form.p_patronymic.data not in (None, ''):
            filters.update({stud[3]: filters_form.p_patronymic.data})
            table_name += "{} ".format(filters_form.p_patronymic.data)
        if filters_form.d_discipline_name.data not in (None, ''):
            filters.update({'discipline': filters_form.d_discipline_name.data})
            table_name += "по дисциплине {} "\
                          .format(filters_form.d_discipline_name.data)
        page = 1
        session['filters_mark'] = filters
        session['table_name_mark'] = table_name

    req = requests.post(curent_api_part + 'marks',
                        json={'filters': filters, 'page': page})
    show_lines = json.loads(req.text)
    # Get page numbers for paginate
    (link_pages) = paginate_func(table_name=db_table_names['mark'],
                                  filters=filters, page=int(page),
                                  count_neighbor=2)
    link = '/marks/page='
    return render_template("marks_select.html",
                           table_name=table_name,
                           column_headers=marks_column_headers,
                           show_lines=show_lines,
                           title=Marks.table_name['marks'],
                           forms=[filters_form],
                           link=link,
                           link_pages=link_pages,
                           buttons=Marks.buttons)


# Добавление новой оценки
@main.route('/mark_add', methods=['GET', 'POST'])
def mark_add():
    clean_session([])  # Удаляем сессионные фильтры
    add_mark = FormAddMark()
    # Фильтры:
    stud = db_column_names[db_table_names['stud']]
    disc = db_column_names[db_table_names['disc']]
    mark = db_column_names[db_table_names['mark']]
    if add_mark.validate_on_submit():
        mark_dict = {stud[0]: add_mark.s_stud_id.data,
                     disc[0]: add_mark.d_discipline_id.data,
                     mark[1]: add_mark.m_mark.data}
        req = requests.post(curent_api_part + 'mark_add', json=mark_dict)
        message = json.loads(req.text)
        flash(message)
        if req.status_code == status.HTTP_201_CREATED:
            return redirect('/marks')
        else:
            return redirect('/mark_add')

    return render_template("add_edit_value.html",
                           table_name="Добавление оценки",
                           title="Добавление оценки",
                           forms=[add_mark])


# Редактирование оценки
@main.route('/mark_edit/<mark_id>/<mark>', methods=['GET', 'POST'])
def mark_edit(mark_id, mark):
    table_name = "Редактирование информации об оценке № " + mark_id
    edit_mark = FormEditMark()
    edit_mark.set_choices(mark)
    if edit_mark.validate_on_submit():
        mark_name = db_column_names[db_table_names['mark']][:2]
        mark_dict = {mark_name[0]: mark_id, mark_name[1]:
                     edit_mark.m_mark.data}
        req = requests.put(curent_api_part + 'mark_edit', json=mark_dict)
        message = json.loads(req.text)['Message']
        flash(message)
        return redirect('/marks')

    return render_template("add_edit_value.html",
                           table_name=table_name,
                           title="Редактирование оценки",
                           forms=[edit_mark])


# Удаление оценки
@main.route('/mark_del/<mark_id>', methods=['GET', 'POST'])
def mark_del(mark_id):
    del_id = {db_column_names[db_table_names['mark']][0]: mark_id}
    req = requests.delete(curent_api_part + 'mark_del', json=del_id)
    message = json.loads(req.text)['Message']
    flash(message)
    return redirect('/marks')
