from __future__ import print_function # In python 2.7
from flask import Flask, render_template, redirect, url_for, request
import os
import sys
import traceback

app = Flask(__name__)

import common

@app.route("/run", methods = ['POST'])
def run_update():
    try:
        print("In run updates !!", file=sys.stderr)
        print(str(request.values), file=sys.stderr)
        records = int(request.form['size'])
        print("Putting entries !!", file=sys.stderr)
        common.put_samples(records)
        print("Putting entries !!", file=sys.stderr)

        return redirect(url_for('hello'))
    except:
        traceback.print_exc(file=sys.stderr)
        print("Exception in run !!" + traceback.format_exc())


@app.route("/")
@app.route("/index")
def hello():
    print("In hello!!", file=sys.stderr)
    samples = common.get_samples()
    print("Got samples", file=sys.stderr)
    return render_template('index.html',
                           samples=samples,
                           count=len(samples))


if __name__ == "__main__":
    app.run(host="0.0.0.0")
