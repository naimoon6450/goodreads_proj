from flask import Flask
from flask_cors import CORS, cross_origin
# from flask_session import Session

import os
app = Flask(__name__)
# session = Session()
app.config.from_object(__name__)
app.config['SECRET_KEY'] = os.getenv('GOODREADS_SECRET_KEY')
app.config['SESSION_TYPE'] = 'filesystem'
# session.init_app(app)
CORS(app, support_credentials=True)
