from passlib.context import CryptContext

ALGORITHM: str = "HS256"

pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
