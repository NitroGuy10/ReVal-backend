from dotenv import load_dotenv
load_dotenv()
from os import environ
from flask import Flask, abort, request
from flask_cors import CORS
import json

import analysis
import database
import sentiment


app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    return "<p>Hello, ReVal-backend!</p>"

@app.route("/create", methods=["POST"])
def create():
    request_data = request.get_json()
    if "reviews" in request_data and type(request_data["reviews"]) == str:
        df_json = analysis.create_product_df_json(request_data["reviews"])
        id = database.add_entry(df_json)
        return {"id": id}
    else:
        abort(400)

@app.route("/product/sample")
def sample():
    with open("sample_data_point.json") as in_file:
        return json.load(in_file)

@app.route("/product/<uuid:id>/")
def dataframe(id):
    entry = database.get_entry(id)
    if entry is None:
        abort(404)
    else:
        return json.loads(entry.dataframe)

@app.route("/product/<uuid:id>/mentions_of", methods=["POST"])
def mentions_of(id):
    request_data = request.get_json()
    entry = database.get_entry(id)
    if entry is None:
        abort(404)
    else:
        return analysis.mentions_of(entry.dataframe, request_data["keywords"])
        # return analysis.mentions_of(entry.dataframe, keyword)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=environ["PORT"])
