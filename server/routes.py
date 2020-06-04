import os
from server import app
from betterreads import client
from flask import jsonify, render_template, flash, redirect, render_template, url_for, session, request
from rauth.utils import parse_utf8_qsl

dev_key = os.getenv('GOODREADS_DEV_KEY')
dev_sec = os.getenv('GOODREADS_SECRET_KEY')
# the goodread client
gc = client.GoodreadsClient(dev_key, dev_sec)
# goodreads = client.GoodreadsClient(dev_key, dev_sec)
# gr_service = goodreads.auth_attempt()

def authHelper():
    if (hasattr(gc, 'session')):
        gc.authenticate(access_token=gc.session.access_token, access_token_secret=gc.session.access_token_secret)
    else:
        gc.authenticate()

@app.route("/")
def index():
    return render_template('login.html')

@app.route('/goodreads/login')
def login():
    oauth_callback = url_for('authorized', _external=True)
    params = {'oauth_callback': oauth_callback}

    r = gr_service.get_raw_request_token(params=dict(params))
    data = parse_utf8_qsl(r.content)
    # sets session for the application
    session['goodreads_oauth'] = (data['oauth_token'],
                                data['oauth_token_secret'])
    print("Session Created", session['goodreads_oauth'])
    return redirect(gr_service.get_authorize_url(data['oauth_token'], **params))

@app.route('/goodreads/authorized')
def authorized():
    request_token, request_token_secret = session.pop('goodreads_oauth')
    # check to make sure the user authorized the request
    print(request_token, request_token_secret)
    if not request_token:
        flash('You did not authorize the request')
        return redirect(url_for('index'))

    try:
        # creds = {'request_token': request_token,
        #         'request_token_secret': request_token_secret}
        # params = {'oauth_verifier': request.args['oauth_verifier']}
        # sess = gr_service.get_auth_session(params=params, **creds)
        print(request.args)
    except Exception as e:
        flash('There was a problem logging into GoodReads: ' + str(e))
        return redirect(url_for('index'))

    return redirect(url_for('friends'))


@app.route('/friends')
def friends():
    authHelper()
    # user_name = 'naimz_sauce'
    # authenticate again but with tokens this time
    user_id = gc.user(username='naimoon1993').gid
    gc_req = gc.request_oauth(
        'friend/user.xml', {'id': 76756345})

    # hoss_books = gc.request_oauth(
    #     'review/list?v=2', {'id': '19666582', 'key': dev_key})
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
    # return jsonify(hoss_books)
    return jsonify(info_arr)

@app.route('/reviews')
def reviews():
    authHelper()
    user_id = gc.user(username='naimoon1993').gid
    gc_req = gc.request_oauth(
        'book/show.xml', {'id': '51913115', 'key': dev_key})
    return gc_req

@app.route('/friends_of_friend/<friends_id>')
def friends_of_friend(friends_id):
    authHelper()
    gc_req = gc.request_oauth(
        'friend/user.xml', {'id': friends_id})
    info_arr = []
    for item in gc_req['friends']['user']:
        dict_user = {}
        if item:
            dict_user['name'] = item['name']
            dict_user['goodreads_id'] = item['id']
            dict_user['friends'] = item['friends_count']
            dict_user['reviews_written'] = item['reviews_count']
            info_arr.append(dict_user)
    return jsonify(info_arr)


if __name__ == '__main__':
    app.run()