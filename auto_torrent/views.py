from flask import Flask, request, jsonify
import subprocess
import logging
from functools import wraps
from mongo import MongoConn
import re
import pymongo

import pdb

app = Flask(__name__)

# logging setup
file_handler = logging.FileHandler('app.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

##################### authentification #########################
def check_auth(username, password):
    return username == 'admin' and password == 'secret'

def authenticate():
    message = {'message': "Unable to authenticate."}
    resp = jsonify(message)

    resp.status_code = 401
    resp.headers['WWW-Authenticate'] = 'Basic realm="Example"'

    return resp

def requires_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return authenticate()

        elif not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return wrapper

################### main search resource ###################
@app.route("/search", methods=['PUT'])
def search():

    # url params
    term = request.args.get('term', '').lower()
    season = request.args.get('season', '').lower()
    episode = request.args.get('episode', '').lower()

    # return 404 if required args not present
    required_args = [term, season, episode]
    if not all(arg for arg in required_args):
        return bad_request(help='term, season, and episode are required args')

    # form params
    # term = request.form['term']
    # season = request.form['season']
    # episode = request.form['episode']

    # check if torrent already exists
    # pdb.set_trace()
    # coll = MongoConn().torrents_coll
    # REGEX = re.compile('.*{}.*'.format(term.replace(' ', '.*')))
    # print REGEX
    # match = list(coll.find({'title': {'$regex': REGEX}, 'season': season, 'episode': episode}))
    #
    # if match:
    #     print 'hi'

    # kick off scrapy process
    cmd = 'scrapy crawl pirate -a search_term=placeholder -a season={0} -a episode={1} -o test.json'.format(season, episode)
    cmd = cmd.split()
    cmd[4] = 'search_term={0}'.format(term)
    subprocess.Popen(cmd)

################## error handling #########################
@app.errorhandler(404)
def bad_request(error=None, help=None):
    message = {
            'status': 404,
            'message': 'Bad request: ' + request.url,
    }
    if help:
        message.update({'help': help})

    resp = jsonify(message)
    resp.status_code = 404

    return resp

################# main ######################
if __name__ == "__main__":
    app.run()
