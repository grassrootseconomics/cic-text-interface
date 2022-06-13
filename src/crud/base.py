# standard imports
from typing import Any, Generic, List, Optional, Type, TypeVar, Union

# external imports
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.orm import Session

# local imports
from src.database.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, object_id: int) -> Optional[ModelType]:
        return db.scalars(
            select(self.model).where(self.model.id == object_id).limit(1)
        ).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return (
            db.execute(select(self.model).offset(skip).limit(limit))
            .scalars()
            .all()
        )

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        return self._save_to_database(db, db_obj)

    def update(self, db: Session, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, dict[str, Any]]) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        return self._save_to_database(db, db_obj)

    @staticmethod
    def _save_to_database(db: Session, db_obj):
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, object_id: int) -> ModelType:
        obj = db.get(self.model, object_id)  # type: ignore
        db.delete(obj)
        db.commit()
        return obj

    def count(self, db: Session):
        return db.scalar(select(func.count()).select_from(self.model))
