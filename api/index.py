import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("firebase.json") 
firebase_admin.initialize_app(cred)

db = firestore.client()
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel  

app = FastAPI()

class ParkingSpaceStatus(BaseModel):
    available: bool

@app.get('/parking/{space_id}', response_model=ParkingSpaceStatus)
def get_space_availability(space_id: str):
    doc_ref = db.collection('parking').document(space_id)
    doc = doc_ref.get()
    if doc.exists:
        return ParkingSpaceStatus(available=doc.to_dict()['available'])
    else:
        raise HTTPException(status_code=404, detail="Space not found")

