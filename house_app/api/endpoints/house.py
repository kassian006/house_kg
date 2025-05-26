from house_app.db.models import House
from house_app.db.schema import HouseSchema
from house_app.db.database import SessionLocal
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


house_router = APIRouter(prefix='/house', tags=['House'])

BASE_DIR = Path(__file__).resolve().parent.parent.parent

model_path = BASE_DIR / 'house_price_model_job.pkl'
scaler_path = BASE_DIR / 'scaler.pkl'

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@house_router.post('/', response_model=HouseSchema)
async def create_house(house: HouseSchema, db: Session = Depends(get_db)):
    house_db = House(**house.dict())
    db.add(house_db)
    db.commit()
    db.refresh(house_db)



@house_router.get('/',)
async def list_house(db: Session = Depends(get_db)):
    return db.query(House).all()


@house_router.get('/{house_id}/', response_model=HouseSchema)
async def detail_house(house_id: int, db:Session = Depends(get_db)):
    house = db.query(House).filter(House.id==house_id).first()
    if house is None:
        raise HTTPException(status_code=404, detail='House not found')
    return house


@house_router.put('/{house_id}/', response_model=HouseSchema)
async def update_house(house_id: int,
                        house_data: HouseSchema,
                        db: Session = Depends(get_db)):
    house = db.query(House).filter(House.id==house_id).first()
    if house is None:
        raise HTTPException(status_code=404, detail='House not found')
    for house_key, house_value in house_data.dict().items():
        setattr(house, house_key, house_value)
    db.commit()
    db.refresh(house)
    return house


@house_router.delete('/{house_id}')
async def delete_house(house_id: int, db: Session = Depends(get_db)):
    house = db.query(House).filter(House.id==house_id).first()
    if house is None:
        raise HTTPException(status_code=404, detail='House not found')
    db.delete(house)
    db.commit()
    return {'message': 'This House is Deleted'}


model_columns = [
    'GrLivArea',
    'YearBuilt',
    'GarageCars',
    'TotalBsmtSF',
    'FullBath',
    'OverallQual'
]


@house_router.post('/predict/')
async def predict_price(house: HouseSchema, db: Session = Depends(get_db)):
    input_data = {
    'GrLivArea': house.area,
    'YearBuilt': house.year,
    'GarageCars': house.garage,
    'TotalBsmtSF': house.total_basement,
    'FullBath': house.bath,
    'OverallQual': house.overall_quality
    }
    input_df = pd.DataFrame([input_data])
    scaled_df = scaler.transform(input_df)
    predicted_price = model.predict(scaled_df)[0]
    return {'predicted_price': round(predicted_price)}
