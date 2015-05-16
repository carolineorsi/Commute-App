from flask import Flask, request, render_template, redirect, url_for, jsonify
import transit
import os

SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', "abcdefg")

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def index():
    options, caltrain_arrival = transit.get_times()

    return render_template('index.html',
                           options=options,
                           caltrain_arrival=caltrain_arrival)


@app.route('/override')
def override():
    station_22nd = int(request.args.get('station_22nd'))

    options, caltrain_arrival = transit.get_times(station_22nd)

    return render_template('index.html',
                           options=options,
                           caltrain_arrival=caltrain_arrival)


if __name__ == '__main__':
    PORT = int(os.environ.get("PORT", 5000))
    DEBUG = "NO_DEBUG" not in os.environ
    app.run(debug=DEBUG, host="0.0.0.0", port=PORT)