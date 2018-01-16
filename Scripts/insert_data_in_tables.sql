-- function to generate student FIO
CREATE OR REPLACE FUNCTION get_fio() RETURNS text[] AS $$
DECLARE
    man_surname text[] := '{"Иванов", "Васильев", "Петров", "Смирнов", "Михайлов", "Фёдоров", "Соколов", "Яковлев", "Попов",
            "Андреев", "Алексеев", "Александров", "Лебедев", "Григорьев", "Степанов", "Семёнов", "Павлов",
            "Богданов", "Николаев", "Дмитриев", "Егоров", "Волков", "Кузнецов", "Никитин", "Соловьёв", "Тимофеев",
            "Орлов", "Афанасьев", "Филиппов", "Сергеев", "Захаров", "Матвеев", "Виноградов", "Кузьмин", "Максимов",
            "Козлов", "Ильин", "Герасимов", "Марков", "Новиков", "Морозов", "Романов", "Осипов", "Макаров", "Зайцев",
            "Беляев", "Гаврилов", "Антонов", "Ефимов", "Леонтьев"}';
    man_name text[] :='{"Афанасий", "Артур", "Алексей", "Александр", "Абрам", "Борис", "Богдан", "Вячеслав", "Владислав", "Владимир",
            "Виталий", "Виктор", "Василий", "Валерий", "Валентин", "Вадим", "Григорий", "Глеб", "Герман", "Герасим",
            "Георгий", "Геннадий", "Даниил", "Дмитрий", "Ермак", "Егор", "Евгений", "Илья", "Игорь", "Иван", "Константин",
            "Кирилл", "Леонид", "Михаил", "Марк", "Матвей", "Максим", "Макар", "Николай", "Никита", "Олег", "Петр", "Павел",
            "Руслан", "Сергей", "Семен", "Федор", "Эдуард", "Юрий", "Ярослав"}';
    man_patronymic text[] :='{"Александрович", "Адамович", "Анатольевич", "Аркадьевич", "Алексеевич", "Андреевич", "Артемович", "Альбертович",
                   "Антонович", "Богданович", "Богуславович", "Борисович", "Вадимович", "Васильевич", "Владимирович", "Вячеславович",
                   "Валерьевич", "Викторович", "Геннадиевич", "Георгиевич", "Григорьевич", "Дмитриевич", "Евгеньевич", "Егорович",
                   "Ефимович", "Иванович", "Ильич", "Игоревич", "Иосифович", "Кириллович", "Леонидович", "Львович", "Макарович",
                   "Максимович", "Матвеевич", "Михайлович", "Натанович", "Николаевич", "Олегович", "Павлович", "Петрович", "Платонович",
                    "Робертович", "Романович", "Русланович", "Сергеевич", "Эдуардович", "Юрьевич", "Яковлевич", "Ярославович"}';
    woman_surname text[] :='{"Иванова", "Смирнова", "Кузнецова", "Попова", "Соколова", "Лебедева", "Козлова", "Новикова", "Морозова", "Петрова",
                     "Волкова", "Соловаьева", "Васильева", "Зайцева", "Павлова", "Семенова", "Голубева", "Виноградова", "Богданова",
                     "Воробьева", "Федорова", "Михайлова", "Беляева", "Тарасова", "Белова", "Комарова", "Орлова", "Киселева", "Макарова",
                     "Андреева", "Ковалёва", "Ильина", "Гусева", "Титова", "Кузьмина", "Кудрявцева", "Баранова", "Куликова", "Алексеева",
                     "Степанова", "Яковалева", "Сорокина", "Сергеева", "Романова", "Захарова", "Борисова", "Королева", "Герасимова",
                     "Пономарева", "Григорьева"}';
    woman_name text[] :='{"Антонина", "Анна", "Анастасия", "Алла", "Алиса", "Александра", "Вероника", "Вера", "Василиса", "Варвара", "Валерия",
                          "Валентина", "Галина", "Диана", "Дарья", "Елена", "Екатерина", "Евдокия", "Евгения", "Жанна", "Зоя", "Зинаида",
                          "Ирина", "Инна", "Инга", "Изабелла", "Кристина", "Клара", "Клавдия", "Кира", "Карина", "Камилла", "Любовь",
                          "Лолита", "Лидия", "Лариса", "Мария", "Марина", "Маргарита", "Нина", "Наталия", "Надежда", "Ольга", "Полина",
                          "Роза", "Светлана", "Татьяна", "Тамара", "Юлия", "Яна"}';
    woman_patronymic text[] :='{"Александровна", "Андреевна", "Архиповна", "Алексеевна", "Антоновна", "Аскольдовна", "Альбертовна", "Аркадьевна",
                     "Афанасьевна", "Анатольевна", "Артемовна", "Богдановна", "Болеславовна", "Борисовна", "Вадимовна", "Валентиновна",
                     "Викторовна", "Вячеславовна", "Геннадиевна", "Георгиевна", "Дмитриевна", "Евгеньевна", "Егоровны", "Егоровна",
                     "Ефимовна", "Ивановна", "Игоревна", "Ильинична", "Кузьминична", "Леонидовна", "Леоновна", "Львовна", "Макаровна",
                     "Матвеевна", "Михайловна", "Максимовна", "Мироновна", "Натановна", "Никифоровна", "Ниловна", "Наумовна", "Николаевна",
                     "Олеговна", "Оскаровна", "Павловна", "Романовна", "Станиславовна", "Тарасовна", "Тимофеевна", "Эдуардовна"}';
    out text[];
    index_surname integer;
    index_name integer;
    index_patronymic integer;

BEGIN
    index_surname := GREATEST(1, floor(random()*50));
    index_name = GREATEST(1, floor(random()*50));
    index_patronymic = GREATEST(1, floor(random()*50));
    if floor(random() + 0.5) + 1 = 2 THEN
        out = ARRAY[man_surname[index_surname], man_name[index_name], man_patronymic[index_patronymic]];
    ELSE
        out = ARRAY[woman_surname[index_surname], woman_name[index_name], woman_patronymic[index_patronymic]];
    END IF;
    RETURN out;
END;
$$ LANGUAGE plpgsql;







-- fill the base
CREATE OR REPLACE FUNCTION insert_data_in_tables() RETURNS text AS $$
DECLARE
    stud_id integer := 0;
    discipline_id integer := 0;
    discipline_id_cycle integer;

    faculty_quantity integer := 20;
    specialty_quantity integer := 10;
    students_group_quantity integer := 20;
    course_quantity integer := 5;
    discipline_quantity integer := 100;

    faculty_base text;
    specialty_base text;
    specialty_short text;
    exam_form_mas text[] := ARRAY['Зачет', 'Экзамен'];
    marks_mas text[] := ARRAY['Не зачтено', 'Зачтено', 'Не аттест.', 'Не удовл.', 'Удовл.', 'Хорошо', 'Отлично'];
    exam_form_massiv text[];
    discipline_name_base text;
    variable text;
    group_nom text;
    char_f varchar;
    char_s varchar;
    FIO text[];
    mark text;
    is_done text := 'DONE';

BEGIN
    RAISE NOTICE 'Data are inserting in DB now. The procedure will take a few minutes. Wait please.';
    FOR f IN 10..9 + faculty_quantity LOOP
        char_f := to_char(f, 'FM99');
        faculty_base := 'faculty_' || char_f;  --input faculties

        -- add specialties to base
        FOR s IN 10..9 + specialty_quantity LOOP
            char_s := to_char(s, 'FM99');
            specialty_base := 'f_' || char_f || '_specialty_' || char_s;
            INSERT INTO specialties (faculty, specialty) VALUES (faculty_base, specialty_base);
            --specialty_short := 'f_' || char_f || '_s_' || to_char(9+specialty_quantity, 'FM99');
            specialty_short := 'f_' || char_f || '_s_' || to_char(s, 'FM99');

            -- add disciplines to base
            exam_form_massiv := '{}';
            FOR d in 100..discipline_quantity+99 LOOP
                discipline_name_base :=  specialty_short || '_discipline_' || to_char(d, 'FM99999');
                variable := exam_form_mas[floor(1.5 + random())];
                INSERT INTO disciplines (discipline_name, exam_form, faculty, specialty) VALUES (discipline_name_base,
                variable, faculty_base, specialty_base);
                exam_form_massiv := exam_form_massiv || variable;
            END LOOP;

            FOR k in 1..5 LOOP
                --add students to base
                group_nom := char_f || char_s || '0' || to_char(k, 'FM999999');
                FOR l in 1..students_group_quantity LOOP
                    stud_id := stud_id + 1;
                    -- take fio
                    FIO := get_fio();
                    INSERT INTO students (surname, name, patronymic, group_no, faculty, specialty) VALUES (FIO[1],
                    FIO[2], FIO[3], group_nom, faculty_base, specialty_base);

                    -- add student marks to base
                    discipline_id_cycle := discipline_id;
                    FOR discp in 1..k*floor(discipline_quantity/course_quantity)  LOOP
                        discipline_id_cycle := discipline_id_cycle + 1;

                        IF exam_form_massiv[discipline_id_cycle] = exam_form_mas[1] THEN
                            mark := marks_mas[floor(1.5 + random())];
                        ELSE
                            mark := marks_mas[floor(random()*4+3.5)];
                        END IF;
                        INSERT INTO marks (stud_id, discipline_id, mark) VALUES (stud_id, discipline_id_cycle, mark);
                    END LOOP;
                END LOOP;
            END LOOP;
            discipline_id := discipline_id + discipline_quantity;

        END LOOP;
    END LOOP;
    RETURN is_done;
END;

$$ LANGUAGE plpgsql;

SELECT insert_data_in_tables();