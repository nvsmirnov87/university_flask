#-*- coding: utf-8 -*-
from flask import json
from flask_wtf import Form
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from ..api_1_0.faculties import  faculties_ext, faculties as get_faculties
from ..api_1_0 import specialties, students, disciplines, database, marks
from ..static.project_const_and_func import marks_mas, exam_form_mas


class FormSelectFaculty(Form):
    f_faculty = SelectField('Выберите факультет')
    submit = SubmitField('Выбрать')

    def __init__(self, *args, **kwargs):
        super(FormSelectFaculty, self).__init__(*args, **kwargs)
        choice_faculties = faculties_ext().get_data()
        choice_faculties = json.loads(choice_faculties)
        self.f_faculty.choices = \
            [(facul, facul) for facul in choice_faculties]


class FormAddSpecialty(Form):
    f_faculty = SelectField('Выберите факультет', choices=[])

    def __init__(self, *args, **kwargs):
        super(FormAddSpecialty, self).__init__(*args, **kwargs)
        gett_faculties = get_faculties().get_data()
        gett_faculties = json.loads(gett_faculties)
        gett_faculties = [(i, i) for i in gett_faculties]
        self.f_faculty.choices = gett_faculties
    s_specialty_name = StringField('Введите название специальности',
                                   validators=[DataRequired()])
    submit = SubmitField('Добавить')


class FormEditSpecialty(Form):
    specialty_name = StringField('Введите новое название специальности',
                                 validators=[DataRequired()])
    submit = SubmitField('Изменить')


class FormSelectFacultySpecialty(Form):
    f_faculty = SelectField('Выберите факультет')
    s_specialty = SelectField('Выберите специальность')

    def __init__(self, *args, **kwargs):
        super(FormSelectFacultySpecialty, self).__init__(*args, **kwargs)
        choice_faculties = get_faculties().get_data()
        choice_faculties = json.loads(choice_faculties)
        self.f_faculty.choices = [("Факультет не выбран",
                                   "Факультет не выбран")]
        self.f_faculty.choices.extend(
            [(facul, facul) for facul in choice_faculties])
        self.s_specialty.choices = [("Факультет не выбран",
                                     "Факультет не выбран")]
    submit = SubmitField('Выбрать')


class FormAddDiscipline(Form):
    f_faculty = SelectField('Выберите факультет')
    s_specialty = SelectField('Выберите специальность')
    discipline_name = StringField('Введите название дисциплины',
                                  validators=[DataRequired()])
    exam_form = SelectField('Выберите форму аттестации')

    def __init__(self, *args, **kwargs):
        super(FormAddDiscipline, self).__init__(*args, **kwargs)
        choice_faculties = get_faculties().get_data()
        choice_faculties = json.loads(choice_faculties)
        self.f_faculty.choices = [("Факультет не выбран",
                                   "Факультет не выбран")]
        self.f_faculty.choices.extend(
            [(facul, facul) for facul in choice_faculties])
        self.s_specialty.choices = [("Факультет не выбран",
                                     "Факультет не выбран")]
        self.exam_form.choices = ([(i, i) for i in exam_form_mas])
    submit = SubmitField('Добавить')


class FormEditDiscipline(Form):
    discipline_name = StringField('Введите новое название дисциплины',
                                  validators=[DataRequired()])
    exam_form = SelectField('Выберите форму аттестации', choices=[])

    def __init__(self, *args, **kwargs):
        super(FormEditDiscipline, self).__init__(*args, **kwargs)
        self.exam_form.choices = ([(i, i) for i in exam_form_mas])
    submit = SubmitField('Изменить')


class FormSelectStudents(Form):
    f_faculty = SelectField('Факультет')
    s_specialty = SelectField('Специальность')
    g_group = StringField('Номер группы')
    s_surname = StringField('Фамилия студента')
    n_name = StringField('Имя студента')
    p_patronymic = StringField('Отчество студента')

    def __init__(self, *args, **kwargs):
        super(FormSelectStudents, self).__init__(*args, **kwargs)
        choice_faculties = get_faculties().get_data()
        choice_faculties = json.loads(choice_faculties)
        self.f_faculty.choices = [("Факультет не выбран",
                                   "Факультет не выбран")]
        self.f_faculty.choices.extend(
            [(facul, facul) for facul in choice_faculties])
        self.s_specialty.choices = [("Факультет не выбран",
                                     "Факультет не выбран")]
    submit = SubmitField('Выбрать')


class FormAddStudent(Form):
    f_faculty = SelectField('Факультет')
    s_specialty = SelectField('Специальность')
    g_group = StringField('Номер группы', validators=[DataRequired()])
    s_surname = StringField('Фамилия студента', validators=[DataRequired()])
    n_name = StringField('Имя студента', validators=[DataRequired()])
    p_patronymic = StringField('Отчество студента',
                               validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(FormAddStudent, self).__init__(*args, **kwargs)
        choice_faculties = get_faculties().get_data()
        choice_faculties = json.loads(choice_faculties)
        self.f_faculty.choices = [("Факультет не выбран",
                                   "Факультет не выбран")]
        self.f_faculty.choices.extend(
            [(facul, facul) for facul in choice_faculties])
        self.s_specialty.choices = [("Факультет не выбран",
                                     "Факультет не выбран")]
    submit = SubmitField('Добавить')


class FormEditStudent(Form):
    g_group = StringField('Номер группы', validators=[DataRequired()])
    s_surname = StringField('Фамилия студента', validators=[DataRequired()])
    n_name = StringField('Имя студента', validators=[DataRequired()])
    p_patronymic = StringField('Отчество студента',
                               validators=[DataRequired()])
    submit = SubmitField('Отредактировать')


class FormSelectMarks(Form):
    f_faculty = SelectField('Факультет')
    s_specialty = SelectField('Специальность')
    g_group = StringField('Номер группы')
    s_surname = StringField('Фамилия студента')
    n_name = StringField('Имя студента')
    p_patronymic = StringField('Отчество студента')
    d_discipline_name = StringField('Название дисциплины')

    def __init__(self, *args, **kwargs):
        super(FormSelectMarks, self).__init__(*args, **kwargs)
        choice_faculties = get_faculties().get_data()
        choice_faculties = json.loads(choice_faculties)
        self.f_faculty.choices = [(facul, facul) for facul in choice_faculties]
        self.s_specialty.choices = []
        self.f_faculty.default = self.f_faculty.choices[0][0]
    submit = SubmitField('Выбрать')


class FormAddMark(Form):
    s_stud_id = StringField('id студента', validators=[DataRequired()])
    d_discipline_id = StringField('id дисциплины', validators=[DataRequired()])
    m_mark = SelectField('Оценка')

    def __init__(self, *args, **kwargs):
        super(FormAddMark, self).__init__(*args, **kwargs)
        self.m_mark.choices = [(i, i) for i in marks_mas]
        self.m_mark.default = marks_mas[0]
    submit = SubmitField('Добавить оценку')


class FormEditMark(Form):
    m_mark = SelectField('Выберите оценку', choices=[])
    submit = SubmitField('Изменить оценку')

    def set_choices(self, mark):
        if mark in marks_mas[:2]:
            self.m_mark.choices = [(i, i) for i in marks_mas[:2]]
        elif mark in marks_mas[2:]:
            self.m_mark.choices = [(i, i) for i in marks_mas][2:]