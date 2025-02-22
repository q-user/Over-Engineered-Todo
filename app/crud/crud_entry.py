from typing import Dict, Union, Any

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.ToDoEntry import ToDoEntry
from app.schemas.todo_entry import TodoEntryCreate, TodoEntryUpdate

# investigate jsonable_encoder from fastapi.encoders


class CRUDToDoEntry(CRUDBase[ToDoEntry, TodoEntryCreate, TodoEntryUpdate]):
    """
    Overrides the update method from CRUDBase to update the is_complete prop
    """
    def update(
        self,
        db: Session,
        *,
        db_obj: ToDoEntry,
        obj_in: Union[TodoEntryUpdate, Dict[str, Any]]
    ) -> ToDoEntry:

        updated_obj = db_obj
        updated_obj.is_complete = obj_in.is_complete

        db.add(updated_obj)
        db.commit()
        db.refresh(updated_obj)
        return updated_obj


todo_entry = CRUDToDoEntry(ToDoEntry)
