CREATE SEQUENCE specialty_ids;
CREATE SEQUENCE discipline_ids;
CREATE SEQUENCE student_ids;
CREATE SEQUENCE mark_ids;

CREATE TABLE specialties(
    specialty_id INTEGER DEFAULT NEXTVAL('specialty_ids'),
    faculty VARCHAR(100) NOT NULL,
    specialty VARCHAR(100) NOT NULL,
    PRIMARY KEY (faculty, specialty)
    );

CREATE TABLE disciplines(
    discipline_id INTEGER PRIMARY KEY DEFAULT NEXTVAL('discipline_ids'),
    discipline_name VARCHAR(100) NOT NULL,
    exam_form VARCHAR(7) NOT NULL,
    faculty VARCHAR(100),
    specialty VARCHAR(100),
    FOREIGN KEY (faculty, specialty) REFERENCES specialties (faculty, specialty)  ON UPDATE CASCADE ON DELETE CASCADE
    );

CREATE TABLE students(
    stud_id INTEGER PRIMARY KEY DEFAULT NEXTVAL('student_ids'),
    surname VARCHAR(30) NOT NULL,
    name VARCHAR(30) NOT NULL,
    patronymic VARCHAR(30)  NOT NULL,
    group_no VARCHAR(15)  NOT NULL,
    faculty VARCHAR(100),
    specialty VARCHAR(100),
    FOREIGN KEY (faculty, specialty) REFERENCES specialties (faculty, specialty)  ON UPDATE CASCADE ON DELETE CASCADE
    );

CREATE TABLE marks(
    mark_id INTEGER DEFAULT NEXTVAL('mark_ids'),
    mark VARCHAR(10) NOT NULL,
    stud_id INTEGER REFERENCES students ON UPDATE CASCADE ON DELETE CASCADE,
    discipline_id INTEGER,
    PRIMARY KEY (stud_id, discipline_id),
    FOREIGN KEY (discipline_id) REFERENCES disciplines (discipline_id)  ON UPDATE CASCADE ON DELETE CASCADE
    );