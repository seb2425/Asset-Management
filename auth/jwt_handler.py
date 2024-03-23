import time
import jwt
from decouple import config #used to rad config files

jwt_secret=config("secret")  #cconfig reads the env file
jwt_algo=config("algorithm")

#function to return generated token by jwt
def token_response(token:str):
    return {"token":token}

#function to sign jwt
def encode_jwt(userID:str):
    payload={
        "userID":userID,
        "expiry":time.time()+2000
    }
    token=jwt.encode(payload,jwt_secret,jwt_algo);
    return token_response(token)

async def decode_jwt(encoded_token:str):
    decoded_token=jwt.decode(encoded_token,jwt_secret,jwt_algo)
    if(decoded_token['expiry']>=time.time()):
        return decoded_token
    return None