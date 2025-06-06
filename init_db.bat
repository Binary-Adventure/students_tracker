@echo off
echo Initializing database...

REM Create tables
echo Creating tables...
psql -U postgres -d college_students_db -f data/db_init.sql

REM Wait for tables to be created
timeout /t 2 > nul

REM Load sample data
echo Loading sample data...
psql -U postgres -d college_students_db -f data/sample_data.sql

echo Initialization complete!
pause