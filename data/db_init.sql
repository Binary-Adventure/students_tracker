-- Database initialization script for college_students_db

-- Create database (run this separately if needed)
-- CREATE DATABASE college_students_db;

-- Create tables
CREATE TABLE IF NOT EXISTS students (
    student_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    group_name VARCHAR(20) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS subjects (
    subject_id SERIAL PRIMARY KEY,
    subject_name VARCHAR(100) NOT NULL,
    teacher_name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS grades (
    grade_id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(student_id) ON DELETE CASCADE,
    subject_id INTEGER REFERENCES subjects(subject_id) ON DELETE CASCADE,
    grade INTEGER CHECK (grade BETWEEN 1 AND 5),
    date DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS attendance (
    attendance_id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(student_id) ON DELETE CASCADE,
    subject_id INTEGER REFERENCES subjects(subject_id) ON DELETE CASCADE,
    is_present BOOLEAN NOT NULL,
    date DATE NOT NULL
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_grades_student_id ON grades(student_id);
CREATE INDEX IF NOT EXISTS idx_grades_subject_id ON grades(subject_id);
CREATE INDEX IF NOT EXISTS idx_grades_date ON grades(date);

CREATE INDEX IF NOT EXISTS idx_attendance_student_id ON attendance(student_id);
CREATE INDEX IF NOT EXISTS idx_attendance_subject_id ON attendance(subject_id);
CREATE INDEX IF NOT EXISTS idx_attendance_date ON attendance(date);

-- Add sample data (uncomment if needed)
/*
-- Sample students
INSERT INTO students (first_name, last_name, group_name, email) VALUES
('Иван', 'Иванов', 'ИС-101', 'ivanov@example.com'),
('Мария', 'Петрова', 'ИС-101', 'petrova@example.com'),
('Алексей', 'Сидоров', 'ИС-102', 'sidorov@example.com'),
('Екатерина', 'Смирнова', 'ИС-102', 'smirnova@example.com');

-- Sample subjects
INSERT INTO subjects (subject_name, teacher_name) VALUES
('Математика', 'Петров П.П.'),
('Информатика', 'Сидорова С.С.'),
('Физика', 'Иванова И.И.'),
('Английский язык', 'Кузнецова К.К.');

-- Sample grades
INSERT INTO grades (student_id, subject_id, grade, date) VALUES
(1, 1, 4, '2023-09-10'),
(1, 2, 5, '2023-09-11'),
(2, 1, 3, '2023-09-10'),
(2, 2, 4, '2023-09-11');

-- Sample attendance
INSERT INTO attendance (student_id, subject_id, is_present, date) VALUES
(1, 1, true, '2023-09-10'),
(1, 2, true, '2023-09-11'),
(2, 1, false, '2023-09-10'),
(2, 2, true, '2023-09-11');
*/