-- Sample data for college_students_db

-- Sample students
INSERT INTO students (first_name, last_name, group_name, email) VALUES
('Ivan', 'Ivanov', 'IS-101', 'ivanov@example.com'),
('Maria', 'Petrova', 'IS-101', 'petrova@example.com'),
('Alexey', 'Sidorov', 'IS-102', 'sidorov@example.com'),
('Ekaterina', 'Smirnova', 'IS-102', 'smirnova@example.com'),
('Dmitry', 'Kozlov', 'IS-101', 'kozlov@example.com'),
('Anna', 'Novikova', 'IS-103', 'novikova@example.com'),
('Sergey', 'Morozov', 'IS-103', 'morozov@example.com'),
('Olga', 'Volkova', 'IS-102', 'volkova@example.com');

-- Sample subjects
INSERT INTO subjects (subject_name, teacher_name) VALUES
('Mathematics', 'Petrov P.P.'),
('Informatics', 'Sidorova S.S.'),
('Physics', 'Ivanova I.I.'),
('English', 'Kuznetsova K.K.'),
('Programming', 'Sokolov A.V.'),
('Database', 'Morozova E.N.');

-- Sample grades
INSERT INTO grades (student_id, subject_id, grade, date) VALUES
(1, 1, 4, '2023-11-01'),
(1, 2, 5, '2023-11-02'),
(1, 3, 3, '2023-11-03'),
(1, 4, 4, '2023-11-04'),
(1, 5, 5, '2023-11-05'),
(1, 6, 4, '2023-11-06'),

(2, 1, 3, '2023-11-01'),
(2, 2, 4, '2023-11-02'),
(2, 3, 5, '2023-11-03'),
(2, 4, 4, '2023-11-04'),
(2, 5, 3, '2023-11-05'),
(2, 6, 4, '2023-11-06'),

(3, 1, 5, '2023-11-01'),
(3, 2, 5, '2023-11-02'),
(3, 3, 4, '2023-11-03'),
(3, 4, 3, '2023-11-04'),
(3, 5, 5, '2023-11-05'),
(3, 6, 5, '2023-11-06'),

(4, 1, 4, '2023-11-01'),
(4, 2, 3, '2023-11-02'),
(4, 3, 4, '2023-11-03'),
(4, 4, 5, '2023-11-04'),
(4, 5, 4, '2023-11-05'),
(4, 6, 3, '2023-11-06');

-- Sample attendance
INSERT INTO attendance (student_id, subject_id, is_present, date) VALUES
(1, 1, true, '2023-11-01'),
(1, 2, true, '2023-11-02'),
(1, 3, false, '2023-11-03'),
(1, 4, true, '2023-11-04'),
(1, 5, true, '2023-11-05'),
(1, 6, true, '2023-11-06'),

(2, 1, false, '2023-11-01'),
(2, 2, true, '2023-11-02'),
(2, 3, true, '2023-11-03'),
(2, 4, true, '2023-11-04'),
(2, 5, false, '2023-11-05'),
(2, 6, true, '2023-11-06'),

(3, 1, true, '2023-11-01'),
(3, 2, true, '2023-11-02'),
(3, 3, true, '2023-11-03'),
(3, 4, false, '2023-11-04'),
(3, 5, true, '2023-11-05'),
(3, 6, true, '2023-11-06'),

(4, 1, true, '2023-11-01'),
(4, 2, false, '2023-11-02'),
(4, 3, true, '2023-11-03'),
(4, 4, true, '2023-11-04'),
(4, 5, true, '2023-11-05'),
(4, 6, false, '2023-11-06');