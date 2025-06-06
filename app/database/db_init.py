import psycopg2
from .db_connect import get_connection

def create_tables():
    """
    Create the necessary tables in the database if they don't exist
    """
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Create students table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id SERIAL PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            group_name VARCHAR(20) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL
        );
        """)
        
        # Create subjects table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            subject_id SERIAL PRIMARY KEY,
            subject_name VARCHAR(100) NOT NULL,
            teacher_name VARCHAR(100) NOT NULL
        );
        """)
        
        # Create grades table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS grades (
            grade_id SERIAL PRIMARY KEY,
            student_id INTEGER REFERENCES students(student_id) ON DELETE CASCADE,
            subject_id INTEGER REFERENCES subjects(subject_id) ON DELETE CASCADE,
            grade INTEGER CHECK (grade BETWEEN 1 AND 5),
            date DATE NOT NULL
        );
        """)
        
        # Create attendance table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            attendance_id SERIAL PRIMARY KEY,
            student_id INTEGER REFERENCES students(student_id) ON DELETE CASCADE,
            subject_id INTEGER REFERENCES subjects(subject_id) ON DELETE CASCADE,
            is_present BOOLEAN NOT NULL,
            date DATE NOT NULL
        );
        """)
        
        conn.commit()
        print("Database tables created successfully")
        return True
    
    except psycopg2.Error as e:
        print(f"Error creating tables: {e}")
        conn.rollback()
        return False
    
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    create_tables()