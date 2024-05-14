from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Text

class SamplePayload(BaseModel):
 __tablename__ = "sample_db_table"
sample_p_key = Column(String, primary_key=True, index=True)
sample_value = Column(Text)


class KeyValueCreate(BaseModel):
 key: str
 value: str

class KeyValueUpdate(BaseModel):
 value: str
