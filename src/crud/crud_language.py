# local imports
from src.crud.base import CRUDBase
from src.models.language import Language
from src.schemas.language import LanguageCreate, LanguageUpdate


class CRUDLanguage(CRUDBase[Language, LanguageCreate, LanguageUpdate]):
    ...


language = CRUDLanguage(Language)
