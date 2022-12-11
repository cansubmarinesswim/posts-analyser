import requests

response = requests.get(
    f"http://127.0.0.1:5000/posts"
)
print(response.text)



response = requests.post(
    f"http://127.0.0.1:5000/post/create"
)
print(response.status_code)

response = requests.post(
    f"http://127.0.0.1:5000/post/create",
    data={
        "post": "blabla"
    }
)
print(response.text, response.status_code)

response = requests.get(
    f"http://127.0.0.1:5000/post/2"
)
print(response.text, response.status_code)