import os
from server import app
from betterreads import client

dev_key = os.getenv('GOODREADS_DEV_KEY')
dev_sec = os.getenv('GOODREADS_SECRET_KEY')
gc = client.GoodreadsClient(dev_key, dev_sec)
gc.authenticate()

@app.route("/")
def index():
    return "Hello World"

@app.route('/hello')
def hello():
    
    user_id = 'naimz_sauce'
    return gc.book(1)
