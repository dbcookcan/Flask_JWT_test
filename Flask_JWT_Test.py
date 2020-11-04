#!/usr/bin/python3
# Flask_JWT_test
# JWT POC code
# David Cook, Nov 2020
#
from flask import Flask, jsonify, request, make_response
import jwt
import datetime
from functools import wraps
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


app = Flask(__name__)
app.config['SECRET_KEY'] = '[LAHJC;F?4R$[m4Lvm:g8WN?'

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per minute", "10 per second"],
)

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
@limiter.limit("")
def unprotected():
    return jsonify({'message' : 'Anyone can view this'})


@app.route('/protected')
@limiter.limit("")
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

