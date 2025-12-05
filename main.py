from fastapi import FastAPI, Depends, HTTPException, status, Body
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import model
from .session import VehiclesDB
import uuid

app = FastAPI()
db = VehiclesDB()

@app.get("/vehicle", status_code=status.HTTP_200_OK)
def read_all_vehicles(db: Session = Depends(db.get_session)):
    vehicles = db.query(model.Vehicles).all()
    return [
        {
            "vin": v.vin,
            "manufacturer_name": v.manufacturer_name,
            "description": v.description,
            "horse_power": v.horse_power,
            "model_name": v.model_name,
            "model_year": v.model_year,
            "purchase_price": v.purchase_price,
            "fuel_type": v.fuel_type 
        }
        for v in vehicles
    ]

@app.post("/vehicle", status_code=status.HTTP_201_CREATED)
def add_vehicle(db:Session = Depends(db.get_session), payload: dict = Body(...)):
    check_formatting(payload)
    for _ in range(10):
        generated_vin = uuid.uuid4().hex[:17].upper()
        vehicle = model.Vehicles()
        for val in payload:
            setattr(vehicle, val, payload[val])
        setattr(vehicle, "vin", generated_vin)
        db.add(vehicle)
        try:
            db.commit()
            db.refresh(vehicle)
            return {
                "vin": vehicle.vin,
                "manufacturer_name": vehicle.manufacturer_name,
                "description": vehicle.description,
                "horse_power": vehicle.horse_power,
                "model_name": vehicle.model_name,
                "model_year": vehicle.model_year,
                "purchase_price": vehicle.purchase_price,
                "fuel_type": vehicle.fuel_type 
            }

        except IntegrityError:
            db.rollback()
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@app.get("/vehicle/{vin}", status_code=status.HTTP_200_OK)
def get_vehicle_by_vin(vin: str, db:Session = Depends(db.get_session)):
    vehicle = db.query(model.Vehicles).filter(model.Vehicles.vin.ilike(vin)).first()
    if not vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {
        "vin": vehicle.vin,
        "manufacturer_name": vehicle.manufacturer_name,
        "description": vehicle.description,
        "horse_power": vehicle.horse_power,
        "model_name": vehicle.model_name,
        "model_year": vehicle.model_year,
        "purchase_price": vehicle.purchase_price,
        "fuel_type": vehicle.fuel_type 
    } 

@app.put("/vehicle/{vin}", status_code=status.HTTP_200_OK)
def update_vehicle(vin: str, payload: dict = Body(...), db: Session = Depends(db.get_session)):
    check_formatting(payload)
    vehicle = db.query(model.Vehicles).filter(model.Vehicles.vin.ilike(vin)).first()
    if not vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    for val in payload:
            setattr(vehicle, val, payload[val])
    db.commit()
    db.refresh(vehicle)
    return {
        "vin": vehicle.vin,
        "manufacturer_name": vehicle.manufacturer_name,
        "description": vehicle.description,
        "horse_power": vehicle.horse_power,
        "model_name": vehicle.model_name,
        "model_year": vehicle.model_year,
        "purchase_price": vehicle.purchase_price,
        "fuel_type": vehicle.fuel_type 
    } 

@app.delete("/vehicle/{vin}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vehicle(vin: str, db: Session = Depends(db.get_session)):
    vehicle = db.query(model.Vehicles).filter(model.Vehicles.vin.ilike(vin)).first()
    if not vehicle:
        return
    db.delete(vehicle)
    db.commit()
    return

@app.exception_handler(RequestValidationError)
async def not_json_request_error_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content="Request entity needs to be JSON formatted"
    )

def check_formatting(payload: dict):
    if len(payload) == 0:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY)
    if "vin" in payload and not isinstance(payload["vin"], str):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY)
    if "manufacturer_name" in payload and not isinstance(payload["manufacturer_name"], str):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY)
    if "description" in payload and not isinstance(payload["description"], str):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY)
    if "horse_power" in payload and not isinstance(payload["horse_power"], int):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY)
    if "model_name" in payload and not isinstance(payload["model_name"], str):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY)
    if "model_year" in payload and not isinstance(payload["model_year"], int):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY)
    if "purchase_price" in payload and not isinstance(payload["purchase_price"], float):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY)
    if "fuel_type" in payload and not isinstance(payload["fuel_type"], str):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY)