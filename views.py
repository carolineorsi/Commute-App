from flask import Flask, request, render_template, redirect, url_for, jsonify
import transit

app = Flask(__name__)

@app.route('/')
def index():
    options = transit.get_times()

    return render_template('index.html',
                           options=options)


if __name__ == '__main__':
    app.run(debug=True)