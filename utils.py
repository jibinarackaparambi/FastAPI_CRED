from datetime import datetime, timedelta, timezone
from typing import Annotated, Any
from fastapi import Depends, HTTPException, status
import jwt
from uuid import uuid4
from  config import security_settings
from core.security import oauth2_scheme
from database.models import Seller
from database.redis import is_jti_blacklisted
from database.session import session_db


def generate_access_token( data: dict, expiry: timedelta = timedelta(days=1)) -> str:
    payload = {  # Fixed order
        **data,
        "jti": str(uuid4()),
        "exp": datetime.now(timezone.utc) + expiry 
    }
    return jwt.encode(  # payload FIRST, key SECOND
        payload,
        security_settings.JWT_SECRET,
        algorithm=security_settings.JWT_ALGORITHM
    )
            

def decode_access_token(token:str) -> dict:
    try:
        return jwt.decode(
            token,
            security_settings.JWT_SECRET,
            algorithms=[security_settings.JWT_ALGORITHM]
        )
    except jwt.DecodeError:
        raise HTTPException(401, "Invalid token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Expired token")
    except jwt.PyJWKError:
        return None
    except Exception as e:
        return None
    

async def get_access_token(token: Annotated[str, Depends(oauth2_scheme)]) -> dict[str,Any]:
    data = decode_access_token(token=token)
    is_blacklisted = await is_jti_blacklisted(data['jti'])
    if data is None or is_blacklisted:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid access token")
    
    return data

async def current_seller(token_data:Annotated[dict, Depends(get_access_token)], session: session_db):
    return await session.get(Seller, token_data['user']['id'])


current_seller_dep = Annotated[Seller, Depends(current_seller)]