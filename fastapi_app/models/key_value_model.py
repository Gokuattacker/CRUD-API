from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Text
5
class KeyValue(BaseModel):
 __tablename__ = "kvstore_keyvalue"
key = Column(String, primary_key=True, index=True)
value = Column(Text)


class KeyValueCreate(BaseModel):
 key: str
 value: str

class KeyValueUpdate(BaseModel):
 value: str
