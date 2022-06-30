from flask import Flask, jsonify, request, abort
import datetime
import os
import jwt
import functools


JWT_SECRET = os.environ.get('JWT_SECRET', 'abc123abc1234')

APP = Flask(__name__)


countries = [
    {"id": 1, "name": "India", "capital": "Delhi", "area": 513120},
    {"id": 2, "name": "Australia", "capital": "Canberra", "area": 7617930},
    {"id": 3, "name": "Srilanka", "capital": "Colombo", "area": 1010408},
]


def require_jwt(function):
    @functools.wraps(function)
    def decorated_function(*args, **kws):
        if not 'Authorization' in request.headers:
            abort(401)
        data = request.headers['Authorization']
        token = str.replace(str(data), 'bearer ', '')
        try:
            jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        except: 
            abort(401)
        return function(*args, **kws)
    return decorated_function


def get_jwt(user_data):
    exp_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
    payload = {'exp': exp_time,
               'nbf': datetime.datetime.utcnow(),
               'email': user_data['email']}
    return jwt.encode(payload, JWT_SECRET, algorithm='HS256')


def create_next_id(): 
    return max(country["id"] for country in countries) + 1


@APP.get('/')
def running():
    return jsonify("Server Running Fine!!!")


@APP.post("/auth")
def auth():
    request_data = request.get_json()
    email = request_data.get('email')
    password = request_data.get('password')
    if not email:
        return jsonify({"message": "Missing parameter: email"}, 400)
    if not password:
        return jsonify({"message": "Missing parameter: password"}, 400)
    body = {'email': email, 'password': password}
    user_data = body
    return jsonify(token=get_jwt(user_data).decode('utf-8'))


@APP.get("/countries")
@require_jwt
def get_countries():
    return jsonify(countries), 200


@APP.post("/countries")
@require_jwt
def add_country():
    if request.is_json:
        country = request.get_json()
        country["id"] = create_next_id()
        countries.append(country)
        return country, 201
    return {"error": "Request must be JSON"}, 415


if __name__ == '__main__':
    APP.run(host='127.0.0.1', port=8080, debug=True)