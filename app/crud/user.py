import logging

from sqlalchemy.exc import OperationalError
from sqlmodel import Session

from app.core.config import settings
from app.core.security import get_password_hash
from app.models.user import User
from app.models.user import UserCreate

logger = logging.getLogger(__name__)


def create_user(session: Session) -> None:
    create_user_obj: UserCreate = UserCreate(
        email=settings.init.email,
        username=settings.init.username,
        password=settings.init.password.get_secret_value(),
        full_name=settings.init.fullname,
    )

    init_user_obj: User = User.model_validate(
        create_user_obj, update={"hashed_password": get_password_hash(create_user_obj.password)}
    )
    try:
        session.add(init_user_obj)
        session.flush()
        session.commit()

        logger.info("User %s created successfully.", create_user_obj.username)

    except OperationalError as e:
        logger.error("User %s created failed.", create_user_obj.username)
        logger.error("Error: %s", e)

        session.rollback()

        exit(1)
