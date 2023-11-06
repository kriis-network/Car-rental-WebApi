from neo4j import GraphDatabase, Driver, AsyncGraphDatabase, AsyncDriver
import json
from car_rental.model.customer import *


URI = "neo4j+s://3da6e885.databases.neo4j.io:7687"
AUTH = ("neo4j", "M_jBdvj6VIQZoTZvmxin541E1-nU_jAAlEUkDnWHJtI")

# Get connection to database
def _get_connection() -> Driver:
    driver = GraphDatabase.driver(URI, auth=AUTH)
    driver.verify_connectivity()
    return driver

def node_to_json(node):
    node_properties = dict(node.items())
    return node_properties

# Car operations
def find_all_cars():
    with _get_connection().session() as session:
        cars = session.run("MATCH (a:Car) RETURN a;")
        nodes_json = [node_to_json(record["a"]) for record in cars]
        return nodes_json, 'All cars'

def find_car_by_reg(reg):
    with _get_connection().session() as session:
        cars = session.run("MATCH (a:Car) WHERE a.reg=$reg RETURN a;", reg=reg)
        nodes_json = [node_to_json(record["a"]) for record in cars]
        return nodes_json, f'Car with reg number {reg} found'

def save_car(make, model, reg, year, capacity):
    with _get_connection().session() as session:
        cars = session.run("MERGE (a:Car{make: $make, model: $model, reg: $reg, year: $year, capacity:$capacity}) RETURN a;", 
                           make=make, model=model, reg=reg, year=year, capacity=capacity)
        nodes_json = [node_to_json(record["a"]) for record in cars]
        return nodes_json, f'Car with reg number {reg} saved to database'

def update_car(make, model, reg, year, capacity):
    with _get_connection().session() as session:
        cars = session.run("MATCH (a:Car{reg:$reg}) SET a.make=$make, a.model=$model, a.year=$year, a.capacity=$capacity RETURN a;", 
                           reg=reg, make=make, model=model, year=year, capacity=capacity)
        nodes_json = [node_to_json(record["a"]) for record in cars]
        return nodes_json, f'Car with reg number {reg} updated'

def delete_car(reg):
    _get_connection().execute_query("MATCH (a:Car{reg: $reg}) DELETE a;", reg=reg)
    return f'Car with reg number {reg} deleted'

# Booking/renting/returning car
def book_car(customer_id, car_id):
    car, customer = _get_car_and_customer(car_id, customer_id)

    if car['capacity'] == 'Booked':
        return 'Car is already booked'
    elif customer['ordered_car'] != 'None':
        return 'Customer has already booked a car'
    else:
        update_car(car['make'], car['model'], car['reg'], car['year'], capacity='Booked')
        update_customer(customer['name'], customer['age'], customer['address'], car_id, customer['id'])
        return 'Car booked successfully'

def cancel_booking(customer_id, car_id):
    car, customer = _get_car_and_customer(car_id, customer_id)

    if car['capacity'] == 'Booked' and customer['ordered_car'] == car_id:
        update_car(car['make'], car['model'], car['reg'], car['year'], capacity='Available')
        update_customer(customer['name'], customer['age'], customer['address'], 'None', customer['id'])
        return 'Booking canceled successfully'
    else:
        return 'Car is not booked by this customer'

def rent_booked_car(customer_id, car_id):
    car, customer = _get_car_and_customer(car_id, customer_id)

    if car['capacity'] == 'Booked' and customer['ordered_car'] == car_id:
        update_car(car['make'], car['model'], car['reg'], car['year'], capacity='Rented')
        update_customer(customer['name'], customer['age'], customer['address'], car_id, customer['id'])
        return 'Car rented successfully'
    else:
        return 'Car is not booked by this customer'

def return_rented_car(customer_id, car_id):
    car, customer = _get_car_and_customer(car_id, customer_id)

    if car['capacity'] == 'Rented' and customer['ordered_car'] == car_id:
        update_car(car['make'], car['model'], car['reg'], car['year'], capacity='Available')
        update_customer(customer['name'], customer['age'], customer['address'], 'None', customer['id'])
        return 'Car returned successfully'
    else:
        return 'Car is not rented by this customer'

def _get_car_and_customer(car_id, customer_id):
    with _get_connection().session() as session:
        car = session.run("MATCH (a:Car) WHERE a.reg=$reg RETURN a;", reg=car_id)
        car = [node_to_json(record["a"]) for record in car][0]

        customer = session.run("MATCH (a:Customer) WHERE a.id=$id RETURN a;", id=customer_id)
        customer = [node_to_json(record["a"]) for record in customer][0]

    return car, customer
