from pydantic import BaseModel, Field, model_validator
from bson import ObjectId
from datetime import datetime
from typing import Optional

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, ObjectId):
            try:
                return ObjectId(v)
            except Exception:
                raise ValueError(f"Invalid ObjectId: {v}")
        return v

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")

class Calculation(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    operation: str
    result: str
    created_at: int = Field(default_factory=lambda: int(datetime.now().timestamp()))

    @model_validator(mode="before")
    def convert_id_to_string(cls, values):
        # Convertir l'ObjectId en chaîne avant la validation
        if "_id" in values and isinstance(values["_id"], ObjectId):
            values["_id"] = str(values["_id"])
        return values

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
