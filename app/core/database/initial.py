import logging

from sqlmodel import Session

from app.core.config import settings
from app.core.security import get_password_hash
from app.models.user import User
from app.models.user import UserCreate

logger = logging.getLogger(__name__)


async def inject_initial_data(*, session: Session) -> None:
    create_user_obj: UserCreate = UserCreate(
        email=settings.init.email,
        username=settings.init.username,
        password=settings.init.password.get_secret_value(),
        full_name=settings.init.fullname,
    )
    try:
        init_user_obj: User = User.model_validate(
            create_user_obj, update={"hashed_password": get_password_hash(create_user_obj.password)}
        )

        session.add(init_user_obj)
        session.flush()
        session.commit()

    except Exception as e:
        logger.error(e)
