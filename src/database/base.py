# Import all the models, so that Base has them before being
# imported by Alembic
from src.database.base_class import Base
import src.models
