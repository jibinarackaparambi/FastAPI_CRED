from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/seller/token')
delivery_partner_oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/delivery_partner/token')