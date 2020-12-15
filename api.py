from sanic import Sanic
from sanic.response import text

from sanic_jwt import exceptions
from sanic_jwt import initialize
from sanic_jwt.decorators import protected


users = {0: {"username": "adi", "password": "adi123", "user_id": 0}}

username_table = {u.get("username"): u for u in users.values()}
userid_table = {u.get("user_id"): u for u in users.values()}


async def authenticate(request, *args, **kwargs):
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username or not password:
        raise exceptions.AuthenticationFailed("Missing username or password.")

    user = username_table.get(username, None)
    if user is None:
        raise exceptions.AuthenticationFailed("User not found.")

    if password != user.get("password"):
        raise exceptions.AuthenticationFailed("Password is incorrect.")

    return user

app = Sanic("login_server")
initialize(app, authenticate=authenticate)


@app.route('/input', methods=['POST'])
@protected()
async def post_handler(request):
    d = {item.get("name"): item.get(filter(lambda x: "Val" in x, item.keys()).__next__()) for item in request.json}

    return text('POST request - {}'.format(d))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
