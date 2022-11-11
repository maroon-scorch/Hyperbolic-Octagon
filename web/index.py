import io, sys
from main import make
from flask import Flask, Response, request, flash, redirect, render_template, url_for, session
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from flask_session import Session 

app = Flask(__name__)
num = 1
val = 1
# app.secret_key = ''
# app.config["SESSION_PERMANENT"] = True
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)


@app.route("/", methods=['GET', 'POST'])
def index():
    global num
    if request.method == "POST":
        input = request.form.get('layer')
        if input.isnumeric():
            layers = int(input)
            num = layers
    
    return render_template('index.html', num=num)

@app.route('/static/plot.png')
def plot_png():
    global val
    fig = make(8, num)
    val = val + 1
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')