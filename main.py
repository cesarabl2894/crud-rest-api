from flask import Flask, json, request
import services.UserService as userService
import services.GameService as gameService
import services.TransactionService as TransactionService
from services.ResponseService import set_headers

app = Flask(__name__)


@app.route('/user/add', methods=['POST'])
def add_user():
    return set_headers(json.dumps(userService.add_user(request.json)), {'Content-Type': 'application/json'})


@app.route('/user/<gamertag>')
def get_user(gamertag):
    return set_headers(json.dumps(userService.get_user(gamertag)), {'Content-Type': 'application/json'})


@app.route('/users')
def get_users():
    return set_headers(json.dumps(userService.get_all_users()), {'Content-Type': 'application/json'})


@app.route('/user/update', methods=['POST'])
def update_user():
    return set_headers(json.dumps(userService.modify_user(request.json)), {'Content-Type': 'application/json'})


@app.route('/user/delete', methods=['POST'])
def delete_user():
    return set_headers(json.dumps(userService.remove_user(request.json)), {'Content-Type': 'application/json'})


@app.route('/game/add', methods=['POST'])
def add_game():
    return set_headers(json.dumps(gameService.add_game(request.json)), {'Content-Type': 'application/json'})


@app.route('/game/<name>')
def get_game(name):
    return set_headers(json.dumps(gameService.get_game(name)), {'Content-Type': 'application/json'})


@app.route('/games')
def get_games():
    return set_headers(json.dumps(gameService.get_all_games()), {'Content-Type': 'application/json'})


@app.route('/game/update', methods=['POST'])
def update_game():
    return set_headers(json.dumps(gameService.modify_game(request.json)), {'Content-Type': 'application/json'})


@app.route('/game/delete', methods=['POST'])
def delete_game():
    return set_headers(json.dumps(gameService.remove_game(request.json)), {'Content-Type': 'application/json'})


@app.route('/order/add', methods=['POST'])
def add_order():
    return set_headers(json.dumps(TransactionService.add_order(request.json)), {'Content-Type': 'application/json'})


@app.route('/order/<int:order_number>')
def get_order(order_number):
    return set_headers(json.dumps(TransactionService.get_transaction(order_number)),
                       {'Content-Type': 'application/json'})


@app.route('/orders')
def get_orders():
    return set_headers(json.dumps(TransactionService.get_all_transactions()), {'Content-Type': 'application/json'})


@app.route('/order/update', methods=['POST'])
def update_order():
    return set_headers(json.dumps(TransactionService.modify_transaction_status(request.json)),
                       {'Content-Type': 'application/json'})


if __name__ == '__main__':
    app.run(debug=True)
