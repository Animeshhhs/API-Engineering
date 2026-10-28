# API Engineering: Connect Systems and Exchange Data

**API used:** JSONPlaceholder, https://jsonplaceholder.typicode.com (free, no key needed)
**Stack:** Python, requests, Flask, Docker, AWS EC2

## Files
| File | Purpose |
|---|---|
| `api_client.py` | Talks to the external API: GET, POST, JSON parsing, error handling |
| `app.py` | Flask app that uses the client (the "application" in Task 4) |
| `demo.py` | Runs every task in order for the live demo |
| `Dockerfile` | Packages the app into an image |

## Task 1: Explore the API and its documentation
Docs: https://jsonplaceholder.typicode.com/guide/
- **Base URL:** `https://jsonplaceholder.typicode.com`
- **Resources:** `/posts`, `/comments`, `/users`, `/todos`, ...
- **Methods:** GET (read), POST (create), PUT/PATCH (update), DELETE
- **Format:** JSON in and out. **Auth:** none.
- **Try it in the browser first:** open `https://jsonplaceholder.typicode.com/posts/1`
  You will see `{"userId":1,"id":1,"title":"...","body":"..."}`

## Task 2 to 5, in one line each
- **2 GET/POST:** `get_posts`, `get_post`, `create_post` in `api_client.py`
- **3 Parse JSON:** `response.json()` gives Python dicts; `summarise_posts` picks fields
- **4 Integrate:** `app.py` exposes `/posts` etc. and calls the client internally
- **5 Errors:** `APIError` + timeout + 404 + connection failure + invalid input (400)

## Run locally
```bash
pip install -r requirements.txt
python demo.py            # shows Tasks 2, 3, 5
python app.py             # starts the app on http://localhost:5000
```
Test the app:
```bash
curl localhost:5000/posts?limit=3
curl localhost:5000/posts/1
curl localhost:5000/posts/99999                       # -> 404 handled
curl -X POST localhost:5000/posts -H "Content-Type: application/json" \
     -d '{"title":"Hello","body":"From curl"}'        # -> 201
curl -X POST localhost:5000/posts -H "Content-Type: application/json" -d '{}'   # -> 400
```

## Docker
```bash
docker build -t api-engineering .
docker run -d -p 5000:5000 --name api-demo api-engineering
curl localhost:5000/health
```
> On an Apple Silicon Mac, build with `docker build --platform linux/amd64 -t api-engineering .`
> or the image will not run on a standard x86 EC2 instance.

## Push the image (Docker Hub) and run on EC2
**On your laptop**
```bash
docker login
docker tag api-engineering YOUR_DOCKERHUB_USERNAME/api-engineering:v1
docker push YOUR_DOCKERHUB_USERNAME/api-engineering:v1
```

**In the AWS console**
1. EC2 -> Launch instance -> Amazon Linux 2023, `t2.micro` / `t3.micro` (free tier), create/download a key pair.
2. Security group inbound rules: **SSH (22)** from My IP, **Custom TCP 80** from Anywhere (0.0.0.0/0).

**On the EC2 instance** (`ssh -i key.pem ec2-user@<PUBLIC_IP>`)
```bash
sudo dnf install -y docker
sudo systemctl enable --now docker
sudo usermod -aG docker ec2-user && exit      # log in again so the group applies

docker run -d -p 80:5000 --restart unless-stopped --name api-demo \
    YOUR_DOCKERHUB_USERNAME/api-engineering:v1
curl localhost/health
```
Open `http://<PUBLIC_IP>/posts?limit=3` in your browser: that is your final demo.
(`-p 80:5000` means port 80 of the server forwards to port 5000 inside the container.)

## Demo script for the instructor (about 3 minutes)
1. Show the docs page and `/posts/1` in the browser (Task 1).
2. `python demo.py`: walk through GET, POST, parsed output, and the two handled errors.
3. Show `app.py`: "our endpoint calls the client, and one error handler returns clean JSON."
4. Show the EC2 public URL working, plus `docker ps` on the server.
