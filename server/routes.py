import os
from server import app
from betterreads import client
from flask import jsonify, render_template, flash, redirect, render_template, url_for, session, request
from rauth.utils import parse_utf8_qsl

dev_key = os.getenv('GOODREADS_DEV_KEY')
dev_sec = os.getenv('GOODREADS_SECRET_KEY')
# the goodread client
gc = client.GoodreadsClient(dev_key, dev_sec)
goodreads = client.GoodreadsClient(dev_key, dev_sec)
gr_service = goodreads.auth_attempt()

def authHelper():
    if (hasattr(gc, 'session')):
        goodreads.auth_attempt(access_token=goodreads.session.access_token, access_token_secret=goodreads.session.access_token_secret)

@app.route("/")
def index():
    if goodreads.session:
        print('from index post auth', goodreads.session.access_token)
        print('from index post auth tok sec', goodreads.session.access_token_secret)
    # print('req args from index', request.args)
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
    print('from auth route', request_token, request_token_secret)
    if not request_token:
        flash('You did not authorize the request')
        return redirect(url_for('index'))

    try:
        # creds = {'request_token': request_token,
        #         'request_token_secret': request_token_secret}
        # params = {'oauth_token': request.args['oauth_token']}
        # setting the session variables once received here
        goodreads.session = gr_service.get_auth_session(
            request_token, request_token_secret
        )
        goodreads.session.access_token = request_token
        goodreads.session.access_token_secret = request_token_secret
    except Exception as e:
        flash('There was a problem logging into GoodReads: ' + str(e))
        return redirect(url_for('index'))
    return redirect(url_for('index'))


@app.route('/friends')
def friends():
    gc.authenticate()
    # print('from friends page',goodreads.session.access_token)
    # user_name = 'naimz_sauce'
    # authenticate again but with tokens this time
    # user_id = goodreads.user(username='naimoon1993').gid
    print('self init', gc)
    gc_req = gc.auth_user('friend/user.xml', {'id': 76756345})
    print(gc_req)

    # hoss_books = goodreads.request_oauth(
    #     'review/list?v=2', {'id': '19666582', 'key': dev_key})
    # info_arr = []
    # for item in gc_req['friends']['user']:
    #     dict_user = {}
    #     if item:
    #         dict_user['name'] = item['name']
    #         dict_user['goodreads_id'] = item['id']
    #         dict_user['friends'] = item['friends_count']
    #         dict_user['reviews_written'] = item['reviews_count']
    #         info_arr.append(dict_user)

    # ids = [friend['id'] for friend in gc_req['friends']['user']]
    # return jsonify(hoss_books)
    # return jsonify(info_arr)
    return 'hi'

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