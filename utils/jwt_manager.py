from jwt import encode, decode

jwt_key = "h9L6xGbaHcMAZi1ywKNRmYr7VDJvEnSQ"

def create_token(payload: dict) -> str:
    token: str = encode(payload=payload, key=jwt_key, algorithm="HS256")
    return token

def verify_token(token: str) -> dict:
    result = dict
    try:
        result = decode(jwt=token, key=jwt_key, algorithms=["HS256"])
    except Exception as error:
        result = { "error": str(error) }
    return result