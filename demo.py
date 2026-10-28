"""
demo.py  --  Final: Demonstrate the integration
Run:  python demo.py      (prints the result of every task, in order)
"""
import api_client
from api_client import APIError


def heading(text):
    print(f"\n{'=' * 60}\n{text}\n{'=' * 60}")


heading("Task 2a: GET /posts?_limit=3")
posts = api_client.get_posts(3)
print(f"Received {len(posts)} posts. First one:\n{posts[0]}")

heading("Task 2b: POST /posts")
new = api_client.create_post("My first post", "Created from Python via POST")
print("Server replied:", new)

heading("Task 3: Parse JSON -> pick fields + compute word count")
for row in api_client.summarise_posts(posts):
    print(row)

heading("Task 5a: Unsuccessful response (404 - post does not exist)")
try:
    api_client.get_post(99999)
except APIError as e:
    print(f"Handled -> status {e.status_code}: {e.message}")

heading("Task 5b: Network failure (wrong server address)")
original = api_client.BASE_URL
api_client.BASE_URL = "https://this-host-does-not-exist.invalid"
try:
    api_client.get_posts()
except APIError as e:
    print(f"Handled -> status {e.status_code}: {e.message}")
finally:
    api_client.BASE_URL = original

print("\nAll tasks demonstrated. The app never crashed.")
