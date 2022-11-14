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
        links = WikipediaApi.get_links(request.args['title'])
        links.insert(0, request.args['title'])
        nodes = [{"id": link, "name": link} for link in links]
        edges = [{"source": links[0], "target": link} for link in links[1:]]
        data = {}
        data['nodes'] = nodes
        data['links'] = edges
        j = jsonify(data)
        return j
    else:
        redirect("/")