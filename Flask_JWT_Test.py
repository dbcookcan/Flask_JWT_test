#!/usr/bin/python3
from flask import Flask, jsonify, request, make_response
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = '[LAHJC;F?4R$[m4Lvm:g8WN?'


def token_required(f):
    @wraps(f)
    def check_token(*args, **kwargs):
        token = request.args.get('token')

        if not token:
           return jsonify({'message' : 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])

        except:
            return jsonify({'message' : '*** FAIL *** Token is invalid'}), 401

        return f(*args, **kwargs)
 
    return check_token

@app.route('/unprotected')
def unprotected():
    return jsonify({'message' : 'Anyone can view this'})


@app.route('/protected')
@token_required
def protected():
    return jsonify({'message' : 'Token is currently valid'})


@app.route('/login')
def login():
    auth = request.authorization

    if auth and auth.password == 'password':
       token = jwt.encode({'user' : auth.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=10)}, app.config['SECRET_KEY'])
       return jsonify({'token' : token.decode('UTF-8')})

    return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic ralm="Login Required"'})


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)

