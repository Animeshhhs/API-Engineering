"""
api_client.py  --  Tasks 1, 2, 3 and 5
=======================================
A small, reusable client for the JSONPlaceholder REST API
(https://jsonplaceholder.typicode.com). It is a free, public, no-login API
made for practice, so anyone can run this without an API key.

Task 1 -> Explore the API & its documentation (see README.md, section "Task 1")
Task 2 -> GET and POST requests            (get_posts, get_post, create_post)
Task 3 -> Parse JSON responses             (summarise_posts)
Task 5 -> Handle errors                    (APIError + _request)
"""
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"
TIMEOUT = 5  # seconds. Never call an API without a timeout, or your app can hang forever.


class APIError(Exception):
    """One custom error type for every failure.
    The rest of the app only has to catch APIError, not 5 different library errors."""

    def __init__(self, message, status_code=500):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def _request(method, path, **kwargs):
    """Single place where every HTTP call is made (so error handling lives in one spot)."""
    url = f"{BASE_URL}{path}"
    try:
        response = requests.request(method, url, timeout=TIMEOUT, **kwargs)
        response.raise_for_status()      # turns 4xx / 5xx status codes into an exception
        return response.json()           # converts the JSON text into Python dict/list
    except requests.exceptions.Timeout:
        raise APIError("The external API took too long to respond", 504)
    except requests.exceptions.ConnectionError:
        raise APIError("Could not connect to the external API", 503)
    except requests.exceptions.HTTPError:
        code = response.status_code
        if code == 404:
            raise APIError("Resource not found", 404)
        raise APIError(f"External API returned an error (HTTP {code})", 502)
    except ValueError:                   # response body was not valid JSON
        raise APIError("External API returned invalid JSON", 502)


# ---------------- Task 2: GET and POST ----------------
def get_posts(limit=10):
    """GET /posts  -> list of posts. `_limit` is a query parameter."""
    return _request("GET", "/posts", params={"_limit": limit})


def get_post(post_id):
    """GET /posts/{id}  -> one post. A path parameter selects the resource."""
    return _request("GET", f"/posts/{post_id}")


def create_post(title, body, user_id=1):
    """POST /posts  -> creates a post. The data goes in the JSON request body.
    (JSONPlaceholder fakes the save and returns the new object with id 101.)"""
    payload = {"title": title, "body": body, "userId": user_id}
    return _request("POST", "/posts", json=payload)


# ---------------- Task 3: Parse JSON ----------------
def summarise_posts(posts):
    """The API returns a list of dicts. We pick only the fields we need
    and add one computed field (word count)."""
    return [
        {
            "id": p["id"],
            "title": p["title"].title(),
            "words": len(p["body"].split()),
        }
        for p in posts
    ]
