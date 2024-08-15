import sqlite3
from cars_data import cars
from problems_data import problems

def insert_problems(conn):
    c = conn.cursor()

    for problem in problems:
        c.execute('''
            INSERT OR IGNORE INTO problems (problem_name, price)
            VALUES (?, ?)
        ''', (problem["name"], problem["price"]))

def insert_cars(conn):
    c = conn.cursor()

    for car in cars:
        # Insert car data
        c.execute('''
            INSERT OR IGNORE INTO cars (id, car_number, image_url)
            VALUES (?, ?, ?)
        ''', (car["id"], car["number"], car["image"]))

        # Insert car problems and link them in car_problems table
        for problem_name in car["problems"]:
            # Get the problem ID
            c.execute('''
                SELECT id FROM problems WHERE problem_name = ?
            ''', (problem_name,))
            problem_id = c.fetchone()[0]

            # Link car and problem in car_problems table
            c.execute('''
                INSERT OR IGNORE INTO car_problems (car_id, problem_id)
                VALUES (?, ?)
            ''', (car["id"], problem_id))

def main():
    conn = sqlite3.connect('cars.db')

    # Insert problems first
    insert_problems(conn)

    # Insert cars and their related problems
    insert_cars(conn)

    # Commit and close the connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()
