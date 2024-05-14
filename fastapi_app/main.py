from fastapi import FastAPI, HTTPException , Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker ,Session
from models.key_value_model import SamplePayload, KeyValueCreate, KeyValueUpdate

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

SQLALCHEMY_DATABASE_URL = "mysql://roneswar:ABHIgyan@localhost/botguage"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

Base.metadata.create_all(bind=engine)

def get_db():
      db = SessionLocal()
      try:
          yield db
      finally:
          db.close()

@app.post("/create/")
def create_key_value(kv: KeyValueCreate, db: Session = Depends(get_db)):
  db_kv = SamplePayload(sample_p_key=kv.key, sample_value=kv.value)
  db.add(db_kv)
  db.commit()
  db.refresh(db_kv)
  return db_kv

@app.get("/retrieve/{key}")
def read_key_value(key: str, db: Session = Depends(get_db)):
 db_kv = db.query(SamplePayload).filter(SamplePayload.sample_p_key == key).first()
 if db_kv is None:
   raise HTTPException(status_code=404, detail="Key not found")
 return db_kv

@app.put("/update/{key}")
def update_key_value(key: str, kv: KeyValueUpdate, db: Session = Depends(get_db)):
 db_kv = db.query(SamplePayload).filter(SamplePayload.sample_p_key == key).first()
 if db_kv is None:
  raise HTTPException(status_code=404, detail="Key not found")
 db_kv.value = kv.value
 db.commit()
 db.refresh(db_kv)
 return db_kv

@app.delete("/delete/{key}")
def delete_key_value(key: str, db: Session = Depends(get_db)):
 db_kv = db.query(SamplePayload).filter(SamplePayload.sample_p_key == key).first()
 if db_kv is None:
  raise HTTPException(status_code=404, detail="Key not found")
 db.delete(db_kv)
 db.commit()
 return {"message": "Key deleted"}
