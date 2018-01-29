from flask import Flask

app = Flask(__name__)

from pollution_globe import routes
