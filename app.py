#!/usr/bin/python3
'''
Module for API for website majoidea.holberton.us
'''


from flask import Flask, jsonify, make_response, request, abort, render_template
from models import storage
from models.base_model import BaseModel, Base
from models import storage
from datetime import datetime
from models.emails import Email

host = '0.0.0.0'
port = 5000

app = Flask(__name__)

@app.teardown_appcontext
def close_session(exception):
    '''
    Method to close the session
    '''
    storage.close()

@app.errorhandler(404)
def page_not_found(e):
    '''
    Method to be called if the page does not exist
    '''
    return make_response(jsonify({"error": "Page not found"}), 404)

@app.route('/status', strict_slashes=False)
def status():
    '''
    Method to ensure the status of the website deployment
    '''

    return jsonify({"status":"OK"})

@app.route('/email', strict_slashes=False, methods=['POST'])
def input_email():
    post_reqs = request.get_json()
    if post_reqs is None:
        return jsonify({"error": "Not a JSON"}), 400
    elif "email" in post_reqs:
        '''call storage to save email'''
        post_reqs['time_stamp'] = datetime.utcnow()
        email_ad = Email(**post_reqs)
        storage.new(email_ad)
        storage.save()
        return (str(email_ad))
    else:
       return make_request(jsonify({"error": "Not a request"}))

@app.route('/', strict_slashes=False, methods=['POST'])
def input_actors():
    '''
    Method takes in 2 actors, from(start of search), to destination actor
    '''
    post_reqs = request.get_json()
    if post_reqs is None:
        return
    else:
        actor_src = post_reqs["from_actor"]
        actor_dest = post_reqs["to_actor"]
        movie_path = storage.query_searches(actor_src, actor_dest)
        if movie_path is None:
            movie_path = find_bacon(actor_src, actor_dest)
        return render_template('index.html', path=movie_path)
@app.route('/', strict_slashes=False, methods=['GET'])
def output_movie_path():
    '''
    Method for a GET request to output the math from 1 movie to the other
    '''
    return render_template('index.html', path=None)

if __name__ == '__main__':
    app.run(host=host, port=port)
