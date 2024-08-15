from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# Function to fetch cars from the database
def get_cars():
    conn = sqlite3.connect('cars.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cars')
    cars = cursor.fetchall()
    conn.close()
    return cars

# Function to fetch problems for a specific car
def get_problems(car_id):
    conn = sqlite3.connect('cars.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.problem_name, p.price
        FROM problems p
        JOIN car_problems cp ON p.id = cp.problem_id
        WHERE cp.car_id = ?
    ''', (car_id,))
    problems = cursor.fetchall()
    conn.close()
    return [{"problem_name": problem[0], "price": problem[1]} for problem in problems]

# Route for the home page
@app.route('/')
@app.route('/car_list/')
def car_list():
    cars = get_cars()
    car_list = [
        {
            "id": car[0],
            "car_number": car[1],
            "image_url": car[2],
            "urgent": bool(car[3]),
            "problems": get_problems(car[0])
        }
        for car in cars
    ]
    return jsonify(car_list)

if __name__ == '__main__':
    app.run(debug=True)
