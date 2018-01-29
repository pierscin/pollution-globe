import time

from flask import render_template, jsonify

from pollution_globe import app
from pollution_globe.aqicn import AqiRepository
from pollution_globe.utils import normalize_data_for_globe


@app.before_first_request
def initialize_data():
    update_data()


@app.route('/')
def index():
    return render_template('globe.html', title="pollution-globe")


@app.route('/update/')
def update_data():
    quiet_period = 60*60
    timestamp = int(time.time())

    current_data_timestamp = getattr(app, 'timestamp', None)

    if current_data_timestamp is None or current_data_timestamp + quiet_period < timestamp:
        data = AqiRepository.get_data()
        app.globe_data = normalize_data_for_globe(data)
        app.timestamp = timestamp

        return jsonify({'timestamp': timestamp}), 200

    return jsonify({'timestamp': current_data_timestamp}), 202


@app.route('/data/')
def pollution():
    return jsonify(app.globe_data)
