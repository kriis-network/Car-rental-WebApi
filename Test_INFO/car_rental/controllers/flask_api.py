from flask import Flask, request, jsonify
from car_rental import app
from car_rental.model.car import *
from car_rental.model.customer import *
from car_rental.model.employee import *


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Handle POST request logic here
        pass
    else:
        # Handle GET request logic here
        return "Hello, World!"

# Car routes
@app.route('/get_cars', methods=["GET"])
def get_cars():
    return jsonify(find_all_cars())

@app.route('/get_car_by_reg_number', methods=['POST'])
def find_car_by_reg_number():
    data = request.get_json()
    return jsonify(find_car_by_reg(data['reg']))

@app.route('/save_car', methods=["POST"])
def save_car_info():
    data = request.get_json()
    return jsonify(save_car(data['make'], data['model'], data['reg'], data['year'], data['capacity']))

@app.route('/update_car', methods=['PUT'])
def update_car_info():
    data = request.get_json()
    return jsonify(update_car(data['make'], data['model'], data['reg'], data['year'], data['capacity']))

@app.route('/delete_car', methods=['DELETE'])
def delete_car_info():
    data = request.get_json()
    return jsonify(delete_car(data['reg']))

# Customer routes
@app.route('/get_customers', methods=["GET"])
def get_customers():
    return jsonify(find_all_customers())

@app.route('/get_customer_by_id', methods=['POST'])
def find_customer_by_id():
    data = request.get_json()
    return jsonify(find_customer_by_id(data['id']))

@app.route('/save_customer', methods=["POST"])
def save_customer_info():
    data = request.get_json()
    return jsonify(save_customer(data['name'], data['age'], data['address'], data['ordered_car'], data['id']))

@app.route('/update_customer', methods=['PUT'])
def update_customer_info():
    data = request.get_json()
    return jsonify(update_customer(data['name'], data['age'], data['address'], data['ordered_car'], data['id']))

@app.route('/delete_customer', methods=['DELETE'])
def delete_customer_info():
    data = request.get_json()
    delete_customer(data['id'])
    return jsonify(find_all_customers())

# Employee routes
@app.route('/get_employees', methods=["GET"])
def get_employees():
    return jsonify(find_all_employees())

@app.route('/get_employee_by_id', methods=['POST'])
def find_employee_by_id():
    data = request.get_json()
    return jsonify(find_employee_by_id(data['id']))

@app.route('/save_employee', methods=["POST"])
def save_employee_info():
    data = request.get_json()
    return jsonify(save_employee(data['name'], data['address'], data['branch'], data['id']))

@app.route('/update_employee', methods=['PUT'])
def update_employee_info():
    data = request.get_json()
    return jsonify(update_employee(data['name'], data['address'], data['branch'], data['id']))

@app.route('/delete_employee', methods=['DELETE'])
def delete_employee_info():
    data = request.get_json()
    delete_employee(data['id'])
    return jsonify(find_all_employees())

# Booking/renting/returning car routes
@app.route('/order-car/<customer_id>/<car_id>', methods=['PUT'])
def order_car_route(customer_id, car_id):
    return jsonify(book_car(customer_id, car_id))

@app.route('/cancel-order/<customer_id>/<car_id>', methods=['PUT'])
def cancel_order_route(customer_id, car_id):
    return jsonify(cancel_booking(customer_id, car_id))

@app.route('/rent-car/<customer_id>/<car_id>', methods=['PUT'])
def rent_car_route(customer_id, car_id):
    return jsonify(rent_booked_car(customer_id, car_id))

@app.route('/return-car/<customer_id>/<car_id>', methods=['PUT'])
def return_car_route(customer_id, car_id):
    return jsonify(return_rented_car(customer_id, car_id))

if __name__ == '__main__':
    app.run(debug=True)
