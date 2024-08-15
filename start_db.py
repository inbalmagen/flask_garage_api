import sqlite3

def init_db():
    conn = sqlite3.connect('cars.db')
    c = conn.cursor()

    # Create the cars table with the urgent column
    c.execute('''
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            car_number TEXT UNIQUE NOT NULL,
            image_url TEXT NOT NULL,
            urgent BOOLEAN NOT NULL DEFAULT 0
        )
    ''')

    # Create the problems table
    c.execute('''
        CREATE TABLE IF NOT EXISTS problems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            problem_name TEXT NOT NULL,
            price REAL NOT NULL,
            UNIQUE (problem_name, price)  -- Ensure unique combination of problem and price
        )
    ''')

    # Create the car_problems join table
    c.execute('''
        CREATE TABLE IF NOT EXISTS car_problems (
            car_id INTEGER,
            problem_id INTEGER,
            FOREIGN KEY (car_id) REFERENCES cars(id) ON DELETE CASCADE,
            FOREIGN KEY (problem_id) REFERENCES problems(id) ON DELETE CASCADE,
            PRIMARY KEY (car_id, problem_id)
        )
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Initialize the database
init_db()
