from car_rental import app

if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)

#Database
car = {
    "make": "Honda",
    "model": "Civic",
    "reg": "BB5678",
    "year": "2015",
    "capacity": "Available"
}

customer = {
    "name": "Alice Johnson",
    "age": "28",
    "address": "California",
    "ordered_car": "None",
    "id": "1"
}

employee = {
    "name": "Michael Myers",
    "address": "Mordor",
    "branch": "Illinois",
    "id": "5"
}
