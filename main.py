from flask import Flask, json, request
import services.UserService as userService
import services.GameService as gameService
import services.TransactionService as transactionService
from services.ResponseService import set_headers

app = Flask(__name__)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')

    if len(response.response):
        response.status = str(json.loads(response.response[0].decode('utf-8'))['code'])

    return response


@app.route('/user/add', methods=['POST'])
def add_user():
    return set_headers(json.dumps(userService.add_user(request.json)), {'Content-Type': 'application/json'})


@app.route('/user/<gamertag>')
def get_user(gamertag):
    return set_headers(json.dumps(userService.get_user(gamertag, request.headers)),
                       {'Content-Type': 'application/json'})


@app.route('/users')
def get_users():
    return set_headers(json.dumps(userService.get_all_users(request.headers)), {'Content-Type': 'application/json'})


@app.route('/user/update', methods=['POST'])
def update_user():
    return set_headers(json.dumps(userService.modify_user(request.json, request.headers)),
                       {'Content-Type': 'application/json'})


@app.route('/user/delete', methods=['POST'])
def delete_user():
    return set_headers(json.dumps(userService.remove_user(request.json, request.headers)),
                       {'Content-Type': 'application/json'})


@app.route('/user/isadmin', methods=['GET'])
def is_admin():
    return set_headers(json.dumps(userService.is_admin(request.headers)),
                       {'Content-Type': 'application/json'})


@app.route('/game/add', methods=['POST'])
def add_game():
    return set_headers(json.dumps(gameService.add_game(request.json, request.headers)),
                       {'Content-Type': 'application/json'})


@app.route('/game/<name>')
def get_game(name):
    return set_headers(json.dumps(gameService.get_game(name)), {'Content-Type': 'application/json'})


@app.route('/games')
def get_games():
    return set_headers(json.dumps(gameService.get_all_games()), {'Content-Type': 'application/json'})


@app.route('/game/update', methods=['POST'])
def update_game():
    return set_headers(json.dumps(gameService.modify_game(request.json, request.headers)),
                       {'Content-Type': 'application/json'})


@app.route('/game/delete', methods=['POST'])
def delete_game():
    return set_headers(json.dumps(gameService.remove_game(request.json, request.headers)),
                       {'Content-Type': 'application/json'})


@app.route('/order/add', methods=['POST'])
def add_order():
    return set_headers(json.dumps(transactionService.add_order(request.json)), {'Content-Type': 'application/json'})


@app.route('/order/<int:order_number>')
def get_order_by_order_number(order_number):
    return set_headers(json.dumps(transactionService.get_transaction_by_order_number(order_number, request.headers)),
                       {'Content-Type': 'application/json'})


@app.route('/orders/game/<int:game_id>')
def get_order_by_game_id(game_id):
    return set_headers(json.dumps(transactionService.get_transactions_by_game_id(game_id, request.headers)),
                       {'Content-Type': 'application/json'})


@app.route('/orders/user')
def get_order_by_user_id():
    return set_headers(json.dumps(transactionService.get_transactions_by_user_id(request.headers)),
                       {'Content-Type': 'application/json'})


@app.route('/orders')
def get_orders():
    return set_headers(json.dumps(transactionService.get_all_transactions(request.headers)),
                       {'Content-Type': 'application/json'})


@app.route('/order/update', methods=['POST'])
def update_order():
    return set_headers(json.dumps(transactionService.modify_transaction_status(request.json, request.headers)),
                       {'Content-Type': 'application/json'})


@app.route('/login', methods=['POST'])
def login():
    return set_headers(json.dumps(userService.login(request.json)), {'Content-Type': 'application/json'})


if __name__ == '__main__':
    app.run(debug=True)
