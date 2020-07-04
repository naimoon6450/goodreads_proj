
from server import db
import os
from server import app
from betterreads import client
from flask import jsonify, render_template, flash, redirect, render_template, url_for, session, request
from rauth.utils import parse_utf8_qsl
from bson.json_util import dumps
import copy

# socket import
from flask_socketio import SocketIO, send, emit
# wrapping the app with the socket
socketio = SocketIO(app, cors_allowed_origins="*")

# get db
user_collection = db.user_collection
goodreads_user_coll = db.goodreads_coll

dev_key = os.getenv('GOODREADS_DEV_KEY')
dev_sec = os.getenv('GOODREADS_SECRET_KEY')
# the goodread client

# gc = client.GoodreadsClient(dev_key, dev_sec)
goodreads = client.GoodreadsClient(dev_key, dev_sec)

# gr_service = goodreads.auth_attempt()


def authHelper():
    # if user exists, use the session token / secret from db
    # print(user_collection.find_one({'user_id': }))
    if (hasattr(goodreads, 'session')):
        goodreads.authenticate_with_callback(
            access_token=goodreads.session.access_token, access_token_secret=goodreads.session.access_token_secret)


@app.route("/", methods=["GET"])
def index():
    if (hasattr(goodreads, 'session')):
        return render_template('home.html')
    #     print('from index post auth', goodreads.session.access_token)
    #     print('from index post auth tok sec', goodreads.session.access_token_secret)
    # print('req args from index', request.args)
    return render_template('login.html')


@app.route('/goodreads/login')
def login():
    # send the url to the method
    oauth_callback = url_for('authorized', _external=True)
    params = {'oauth_callback': oauth_callback}

    # r = gr_service.get_raw_request_token(params=dict(params))
    # data = parse_utf8_qsl(r.content)
    data, redir_uri = goodreads.authenticate_with_callback(params=dict(params))
    # sets session for the application
    session['goodreads_oauth'] = (data['oauth_token'],
                                  data['oauth_token_secret'])
    print("Session Created", session['goodreads_oauth'])
    # return redirect(gr_service.get_authorize_url(data['oauth_token'], **params))
    return redirect(redir_uri)


@app.route('/goodreads/authorized')
def authorized():
    request_token, request_token_secret = session.pop('goodreads_oauth')
    # check to make sure the user authorized the request
    creds = {'request_token': request_token,
             'request_token_secret': request_token_secret}
    if not request_token:
        flash('You did not authorize the request')
        return redirect(url_for('index'))

    try:
        # params = {'oauth_token': request.args['oauth_token']}
        # setting the session variables once received here
        # once the user approves, add tokens to session
        goodreads.auth_finalize(request_token, request_token_secret)
    except Exception as e:
        flash('There was a problem logging into GoodReads: ' + str(e))
        return redirect(url_for('index'))

    # get the authenticated user
    goodreads_user_obj = goodreads.auth_user()

    # user_name = goodreads_user_obj.user_name
    user_id = goodreads_user_obj['user']['@id']
    creds.update({'user_id': user_id})

    # if user doesn't exist in db insert
    user_in_db = user_collection.find_one({'user_id': user_id})
    if not user_in_db:
        user_collection.insert_one(creds)

    # return redirect(url_for('index'))
    redir_str = 'http://localhost:3000/home?oauth_token=' + request_token
    return redirect(redir_str)


@app.route('/friends')
def friends():
    authHelper()
    # username = goodreads.auth_user().gid
    gc_friends = goodreads.friends(76756345)
    copy_to_send = copy.deepcopy(gc_friends)
    # also sent to atlassian
    # goodreads_user_coll.remove({})
    # mongo automatically adds the object id into the object, and mutattes the initial friend obj
    # goodreads_user_coll.insert_many(gc_friends)
    # return render_template('friends.html', data=info_arr)
    return jsonify(copy_to_send)


@app.route('/get_friend', methods=["POST"])
def get_friend():
    # get user from atlas db
    user_id_from_client = request.json['goodreads_id']
    user_obj = goodreads_user_coll.find_one(
        {'goodreads_id': user_id_from_client})
    return dumps(user_obj)


@app.route('/reviews')
def reviews():
    authHelper()
    return goodreads.review_for_book('51913115')


@app.route('/friends_of_friend', methods=["POST"])
def friends_of_friend():
    authHelper()
    info_arr = []
    for page in range(1, 5):
        gc_req = goodreads.request_oauth(
            'friend/user.xml', {'id': request.form['friendId'], 'page': page})
        for item in gc_req['friends']['user']:
            dict_user = {}
            if item:
                dict_user['name'] = item['name']
                dict_user['goodreads_id'] = item['id']
                dict_user['friends'] = item['friends_count']
                dict_user['reviews_written'] = item['reviews_count']
                info_arr.append(dict_user)
    return render_template('friends.html', data=info_arr)
    # return jsonify(gc_req)


@app.route('/user_shelves', methods=["POST"])
def user_shelves():
    authHelper()
    gc_req = goodreads.request_oauth(
        'shelf/list.xml', {'key': dev_key, 'user_id': request.form['user_id']})
    shelves = []
    for item in gc_req['shelves']['user_shelf']:
        dict_user = {}
        if item:
            dict_user['shelf_name'] = item['name']
            dict_user['shelf_book_count'] = item['book_count']['#text']
            shelves.append(dict_user)

    return jsonify(shelves)


@app.route('/test')
def test():
    authHelper()
    # gc_req = goodreads.request_oauth('search/index.xml', {'key': dev_key, 'q': 'fire next time'})
    # gc_req = goodreads.request_oauth('review/list?v=2', {'key': dev_key, 'id': '76756345', 'v': 2})
    user = goodreads.user(76756345)
    for review in user.reviews():
        print(goodreads.review(review.gid).body)
    # shelves = []
    # for item in gc_req['shelves']['user_shelf']:
    #     dict_user = {}
    #     if item:
    #         dict_user['shelf_name'] = item['name']
    #         dict_user['shelf_book_count'] = item['book_count']['#text']
    #         shelves.append(dict_user)
    return 'no'


# message route
@socketio.on('message')
def message(data):
    print(f"\n\n{data}\n\n")
    # will by default push message to event bucket "message"
    print('data:', data)
    # send(data, broadcast=True)
    # while(True):
    # emit('message', data, broadcast=True)
    send(data, broadcast=True)


if __name__ == '__main__':
    # app.run()
    socketio.run(app)
