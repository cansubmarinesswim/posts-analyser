import requests

response = requests.get(f"http://127.0.0.1:5000/posts")
print(response.text)


response = requests.post(
    f"http://127.0.0.1:5000/post/add_user",
    data={
        "username": "user1",
        "password": "User123!"
    }
)

response = requests.post(
    f"http://127.0.0.1:5000/post/create",
    data={
        "username": "user1",
        "title": "tytul",
        "post": "Amazing performance"
    }
)
print(response.text, response.status_code)

response = requests.post(
    f"http://127.0.0.1:5000/post/create",
    data={
        "username": "user1",
        "title": "tytul2",
        "post": "OK performance"
    }
)
print(response.text, response.status_code)


response = requests.get(f"http://127.0.0.1:5000/posts")
print(response.text)


response = requests.get(
    f"http://127.0.0.1:5000/post/1"
)
print(response.text, response.status_code)
