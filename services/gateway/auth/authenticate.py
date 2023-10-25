import os
import requests


def token(request):
    if "Authorization" not in request.headers:
        return None, ("missing credentials", 401)
    token = request.headers["Authorization"]
    if not token:
        return None, ("missing credentials", 401)
    response = requests.post(
        f"http://{os.environ.get('AUTH_SERVICE_ADDRESS')}/authenticate",
        headers={"Authorization": token},
    )
    if response.status_code == 200:
        return None, (response.txt, None)
    else:
        return None, (response.txt, response.status_code)
