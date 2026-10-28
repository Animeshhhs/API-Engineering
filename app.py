"""
app.py  --  Task 4: Integrate the API into an application
==========================================================
A Flask web app. Our app has its OWN endpoints; behind the scenes it calls the
external API through api_client.py. This is the usual real-world pattern:

   Browser/Postman  --->  our Flask app  --->  JSONPlaceholder API
                    <---                  <---
"""
from flask import Flask, jsonify, request
import api_client
from api_client import APIError

app = Flask(__name__)


@app.get("/")
def home():
    return jsonify(message="API Engineering demo is running",
                   endpoints=["/health", "/posts", "/posts/<id>", "POST /posts"])


@app.get("/health")
def health():
    # Used to check the container is alive (handy after deploying on EC2).
    return jsonify(status="ok")


@app.get("/posts")
def list_posts():
    limit = request.args.get("limit", default=5, type=int)
    posts = api_client.get_posts(limit)
    return jsonify(api_client.summarise_posts(posts))      # Task 3 used here


@app.get("/posts/<int:post_id>")
def one_post(post_id):
    return jsonify(api_client.get_post(post_id))


@app.post("/posts")
def add_post():
    data = request.get_json(silent=True) or {}
    # Validate input BEFORE calling the external API (Task 5: unsuccessful requests)
    if not data.get("title") or not data.get("body"):
        return jsonify(error="Both 'title' and 'body' are required"), 400
    created = api_client.create_post(data["title"], data["body"], data.get("userId", 1))
    return jsonify(created), 201


# Task 5: one handler turns any APIError into a clean JSON reply with the right status code
@app.errorhandler(APIError)
def handle_api_error(err):
    return jsonify(error=err.message), err.status_code


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
