from flask import Flask, render_template, request, flash, jsonify, redirect
import WikipediaApi

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        return render_template("index.html", title=request.form['title'])

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/api")
def api():
    if (request.args):
        return WikipediaApi.get_links(request.args['title'])
    else:
        redirect("/")