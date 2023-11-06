from flask import Flask

app = Flask('car_rental')

from car_rental.controllers import *