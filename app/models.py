from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime
from typing import Optional

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class Calculation(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    operation: str
    result: str
    created_at: int = Field(default_factory=lambda: int(datetime.now().timestamp()))

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}