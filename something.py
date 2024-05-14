from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

app = FastAPI()

class KeyValue(BaseModel):
    key: str
    value: str

class KeyValueService:
    def create_key_value(self, key_value: KeyValue):
        try:
            KeyValueModel.objects.create(key=key_value.key, value=key_value.value)
            return {"message": "Key-value pair created successfully"}
        except IntegrityError as e:
            raise HTTPException(status_code=400, detail="Key already exists")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def read_key_value(self, key: str):
        try:
            kv_model = KeyValueModel.objects.get(key=key)
            return {"value": kv_model.value}
        except ObjectDoesNotExist:
            raise HTTPException(status_code=404, detail="Key not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def update_key_value(self, key: str, key_value: KeyValue):
        try:
            kv_model = KeyValueModel.objects.get(key=key)
            kv_model.value = key_value.value
            kv_model.save()
            return {"message": "Key-value pair updated successfully"}
        except ObjectDoesNotExist:
            raise HTTPException(status_code=404, detail="Key not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def delete_key_value(self, key: str):
        try:
            KeyValueModel.objects.get(key=key).delete()
            return {"message": "Key-value pair deleted successfully"}
        except ObjectDoesNotExist:
            raise HTTPException(status_code=404, detail="Key not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

key_value_service = KeyValueService