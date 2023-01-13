from flask import Flask, render_template, request, send_from_directory
from werkzeug.exceptions import HTTPException
import WikipediaApi
import os

app = Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 
                                'favicon.ico', mimetype='image/vnd.microsoft.icon')

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
    if ('prop' in request.args):
        if (request.args['prop'] == 'links'):
            return WikipediaApi.get_links(request.args['titles'])
        elif (request.args['prop'] == 'extracts'):
            return WikipediaApi.get_summary(request.args['titles'])
        elif (request.args['prop'] == 'images'):
            return WikipediaApi.get_thumbnail(request.args['titles'])
    elif ('query' in request.args):
        return WikipediaApi.search(request.args['query'])
    else:
        return WikipediaApi.error()