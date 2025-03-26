from sqlmodel import Session


async def inject_initial_data(*, session: Session) -> None:
    ...

    # session.commit()
