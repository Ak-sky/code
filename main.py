from flask import Flask, request, jsonify, make_response
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "akash": generate_password_hash("ibm")
}

countries = [
    {"id": 1, "name": "Thailand", "capital": "Bangkok", "area": 513120},
    {"id": 2, "name": "Australia", "capital": "Canberra", "area": 7617930},
    {"id": 3, "name": "Egypt", "capital": "Cairo", "area": 1010408},
]

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username


def create_next_id(): 
    return max(country["id"] for country in countries) + 1


@app.get("/countries")
@auth.login_required
def get_countries():
    return jsonify(countries)


@app.post("/countries")
@auth.login_required
def add_country():
    if request.is_json:
        country = request.get_json()
        country["id"] = create_next_id()
        countries.append(country)
        return country, 201
    return {"error": "Request must be JSON"}, 415


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)