import os
from server import app
from betterreads import client
from flask import jsonify

dev_key = os.getenv('GOODREADS_DEV_KEY')
dev_sec = os.getenv('GOODREADS_SECRET_KEY')
# the goodread client
gc = client.GoodreadsClient(dev_key, dev_sec)
gc.authenticate()


@app.route("/")
def index():
    gr_token = gc.session.access_token
    gr_sec_token = gc.session.access_token_secret
    return "Hello World"


@app.route('/friends')
def friends():
    # user_name = 'naimz_sauce'
    # authenticate again but with tokens this time
    user_id = gc.user(username='naimz_sauce').gid
    gc_req = gc.request_oauth(
        'friend/user.xml', {'id': user_id})

    hoss_books = gc.request_oauth(
        'review/list?v=2', {'id': '19666582', 'key': dev_key})
    info_arr = []
    for item in gc_req['friends']['user']:
        dict_user = {}
        if item:
            dict_user['name'] = item['name']
            dict_user['goodreads_id'] = item['id']
            dict_user['friends'] = item['friends_count']
            dict_user['reviews_written'] = item['reviews_count']
            info_arr.append(dict_user)

    # ids = [friend['id'] for friend in gc_req['friends']['user']]
    return jsonify(hoss_books)
    # return jsonify(info_arr)
