# scripts/get_jwt_token.py
import json, jwt, time
with open('secrets/keys.json') as f:
    keys = json.load(f)
payload = {
    'sub': keys.get('user', 'superagent'),
    'exp': keys.get('exp', int(time.time()) + 3600)
}
token = jwt.encode(payload, keys['jwt_secret'], algorithm='HS256')
print(token)
