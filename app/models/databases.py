from logging import Logger
from logging import getLogger

from .urls import UrlsBase

logger: Logger = getLogger(__name__)


# Due to SQLAlchemy model, we need to import all database models here
# So when we call SQLModel.metadat, all the database models are imported
# and SQLModel can properly initialize the relationships.

# We use __all__ to prevent the linter from complaining about the import not being used
# and we can also use it to import all the models in a single line in other modules.

# Order by table name, and add comments to make it easier to find the model you need.
__all__ = [
    "UrlsBase",  # URLs Base
]

logger.info("All database models are imported")
