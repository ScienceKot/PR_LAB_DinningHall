from flask import Flask, request
from DinningHall import *
import json

app = Flask(__name__)

dinning_hall = DinningHall(5, 10, 8, 'menu.json')
executor = futures.ThreadPoolExecutor(len(dinning_hall.waiters.waiters))
stars = []
@app.route('/distribution', methods=['POST'])
def distribution():
    global stars
    data = request.json
    elasted_time = dinning_hall.distrubute_order(data)
    if elasted_time < data['max_wait']:
        data['stars'] = 5
    elif elasted_time <= data['max_wait'] * 1.1:
        data['stars'] = 4
    elif elasted_time <= data['max_wait'] * 1.2:
        data['stars'] = 3
    elif elasted_time <= data['max_wait'] * 1.3:
        data['stars'] = 2
    elif elasted_time <= data['max_wait'] * 1.4:
        data['stars'] = 1
    else:
        data['stars'] = 0
    stars.append((data['order_id'], data['stars']))
    return "hi"

@app.route('/', methods=['GET'])
def index():
    global stars
    dinning_hall.generate_orders(4)
    to_do = []
    for order in dinning_hall.waiters.order_list:
        future = executor.submit(dinning_hall.waiters.send_order, order)
        to_do.append(future)
    for future in futures.as_completed(to_do):
        _ = future.result()
    return ''.join([f'<p>Order: {order_id}: {star} stars</p>' for order_id, star in stars])

app.run(port=3000)
