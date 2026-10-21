from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/results")
def results():
    selected_currencies = request.args.getlist("currencies")
    print(selected_currencies)
    return render_template("Currency Results")
