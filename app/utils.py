from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def pwd_hash(password: str):
    return(pwd_context.hash(password))

def pwd_verify(plain_pwd, hashed_pwd):
    return(pwd_context.verify(plain_pwd, hashed_pwd))
