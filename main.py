from flask import Flask, render_template, redirect, url_for
import os
app = Flask(__name__)

import common

@app.route("/run", methods = ['POST'])
def run_update():
    records = int(request.form['size'])
    common.put_samples(records)

    return redirect(url_for('index'))


@app.route("/")
@app.route("/index")
def hello():
    samples = common.get_samples()
    print "Samples are " + samples
    return render_template('index.html',
                           samples=samples,
                           count=len(samples))


if __name__ == "__main__":
    app.run(host="0.0.0.0")
