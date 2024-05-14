from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()

# Replace the below URL with your own database URL
SQLALCHEMY_DATABASE_URL = "mysql://mydatabaseuser:mypassword@localhost/mydatabase"
# For MySQL: "mysql://mydatabaseuser:mypassword@localhost/mydatabase"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class KeyValue(Base):
    __tablename__ = "kvstore_keyvalue"
    key = Column(String, primary_key=True, index=True)
    value = Column(Text)

Base.metadata.create_all(bind=engine)

class KeyValueCreate(BaseModel):
    key: str
    value: str

class KeyValueUpdate(BaseModel):
    value: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/create/")
def create_key_value(kv: KeyValueCreate, db: Session = Depends(get_db)):
    db_kv = KeyValue(key=kv.key, value=kv.value)
    db.add(db_kv)
    db.commit()
    db.refresh(db_kv)
    return db_kv

@app.get("/retrieve/{key}")
def read_key_value(key: str, db: Session = Depends(get_db)):
    db_kv = db.query(KeyValue).filter(KeyValue.key == key).first()
    if db_kv is None:
        raise HTTPException(status_code=404, detail="Key not found")
    return db_kv

@app.put("/update/{key}")
def update_key_value(key: str, kv: KeyValueUpdate, db: Session = Depends(get_db)):
    db_kv = db.query(KeyValue).filter(KeyValue.key == key).first()
    if db_kv is None:
        raise HTTPException(status_code=404, detail="Key not found")
    db_kv.value = kv.value
    db.commit()
    db.refresh(db_kv)
    return db_kv

@app.delete("/delete/{key}")
def delete_key_value(key: str, db: Session = Depends(get_db)):
    db_kv = db.query(KeyValue).filter(KeyValue.key == key).first()
    if db_kv is None:
        raise HTTPException(status_code=404, detail="Key not found")
    db.delete(db_kv)
    db.commit()
    return {"message": "Key deleted"}
