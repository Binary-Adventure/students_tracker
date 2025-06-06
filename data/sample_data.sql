-- Sample data for college_students_db

-- Sample students
INSERT INTO students (first_name, last_name, group_name, email) VALUES
('Иван', 'Иванов', 'ИС-101', 'ivanov@example.com'),
('Мария', 'Петрова', 'ИС-101', 'petrova@example.com'),
('Алексей', 'Сидоров', 'ИС-102', 'sidorov@example.com'),
('Екатерина', 'Смирнова', 'ИС-102', 'smirnova@example.com'),
('Дмитрий', 'Козлов', 'ИС-101', 'kozlov@example.com'),
('Анна', 'Новикова', 'ИС-103', 'novikova@example.com'),
('Сергей', 'Морозов', 'ИС-103', 'morozov@example.com'),
('Ольга', 'Волкова', 'ИС-102', 'volkova@example.com');

-- Sample subjects
INSERT INTO subjects (subject_name, teacher_name) VALUES
('Математика', 'Петров П.П.'),
('Информатика', 'Сидорова С.С.'),
('Физика', 'Иванова И.И.'),
('Английский язык', 'Кузнецова К.К.'),
('Программирование', 'Соколов А.В.'),
('База данных', 'Морозова Е.Н.');

-- Sample grades (current date - 30 days to current date)
INSERT INTO grades (student_id, subject_id, grade, date) VALUES
(1, 1, 4, CURRENT_DATE - INTERVAL '30 days'),
(1, 2, 5, CURRENT_DATE - INTERVAL '29 days'),
(1, 3, 3, CURRENT_DATE - INTERVAL '28 days'),
(1, 4, 4, CURRENT_DATE - INTERVAL '27 days'),
(1, 5, 5, CURRENT_DATE - INTERVAL '26 days'),
(1, 6, 4, CURRENT_DATE - INTERVAL '25 days'),

(2, 1, 3, CURRENT_DATE - INTERVAL '30 days'),
(2, 2, 4, CURRENT_DATE - INTERVAL '29 days'),
(2, 3, 5, CURRENT_DATE - INTERVAL '28 days'),
(2, 4, 4, CURRENT_DATE - INTERVAL '27 days'),
(2, 5, 3, CURRENT_DATE - INTERVAL '26 days'),
(2, 6, 4, CURRENT_DATE - INTERVAL '25 days'),

(3, 1, 5, CURRENT_DATE - INTERVAL '30 days'),
(3, 2, 5, CURRENT_DATE - INTERVAL '29 days'),
(3, 3, 4, CURRENT_DATE - INTERVAL '28 days'),
(3, 4, 3, CURRENT_DATE - INTERVAL '27 days'),
(3, 5, 5, CURRENT_DATE - INTERVAL '26 days'),
(3, 6, 5, CURRENT_DATE - INTERVAL '25 days'),

(4, 1, 4, CURRENT_DATE - INTERVAL '30 days'),
(4, 2, 3, CURRENT_DATE - INTERVAL '29 days'),
(4, 3, 4, CURRENT_DATE - INTERVAL '28 days'),
(4, 4, 5, CURRENT_DATE - INTERVAL '27 days'),
(4, 5, 4, CURRENT_DATE - INTERVAL '26 days'),
(4, 6, 3, CURRENT_DATE - INTERVAL '25 days');

-- Sample attendance (current date - 30 days to current date)
INSERT INTO attendance (student_id, subject_id, is_present, date) VALUES
(1, 1, true, CURRENT_DATE - INTERVAL '30 days'),
(1, 2, true, CURRENT_DATE - INTERVAL '29 days'),
(1, 3, false, CURRENT_DATE - INTERVAL '28 days'),
(1, 4, true, CURRENT_DATE - INTERVAL '27 days'),
(1, 5, true, CURRENT_DATE - INTERVAL '26 days'),
(1, 6, true, CURRENT_DATE - INTERVAL '25 days'),

(2, 1, false, CURRENT_DATE - INTERVAL '30 days'),
(2, 2, true, CURRENT_DATE - INTERVAL '29 days'),
(2, 3, true, CURRENT_DATE - INTERVAL '28 days'),
(2, 4, true, CURRENT_DATE - INTERVAL '27 days'),
(2, 5, false, CURRENT_DATE - INTERVAL '26 days'),
(2, 6, true, CURRENT_DATE - INTERVAL '25 days'),

(3, 1, true, CURRENT_DATE - INTERVAL '30 days'),
(3, 2, true, CURRENT_DATE - INTERVAL '29 days'),
(3, 3, true, CURRENT_DATE - INTERVAL '28 days'),
(3, 4, false, CURRENT_DATE - INTERVAL '27 days'),
(3, 5, true, CURRENT_DATE - INTERVAL '26 days'),
(3, 6, true, CURRENT_DATE - INTERVAL '25 days'),

(4, 1, true, CURRENT_DATE - INTERVAL '30 days'),
(4, 2, false, CURRENT_DATE - INTERVAL '29 days'),
(4, 3, true, CURRENT_DATE - INTERVAL '28 days'),
(4, 4, true, CURRENT_DATE - INTERVAL '27 days'),
(4, 5, true, CURRENT_DATE - INTERVAL '26 days'),
(4, 6, false, CURRENT_DATE - INTERVAL '25 days');