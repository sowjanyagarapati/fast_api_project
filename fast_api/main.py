from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
import pandas as pd
from datetime import datetime

from utils import commonUtils
import models
from db import engine, local_session
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db_ = local_session()
        yield db_
    finally:
        db_.close()

@app.get("/")
def index():
    return "Hello, world!"

@app.post("/upload_file/")
def upload_file(csv_file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        df = pd.read_csv(csv_file.file)
        obj = commonUtils()
        df = obj.clean_df(df)
        for idx, row in df.iterrows():
            cobj = models.Customers()
            cobj.txn = row["txn"]
            cobj.acc_number = row["acc_number"]
            cobj.ifsc_number = row["ifsc_number"]
            cobj.bank_name = row["bank_name"]
            cobj.acc_holder_name = row["acc_holder_name"]
            cobj.txn_type = row["txn_type"]
            cobj.TXN_DATE = datetime.strptime(row["TXN DATE"], "%Y-%m-%d")
            cobj.AMOUNT = row["AMOUNT"]
            db.add(cobj)
            db.commit()
        return {"message": "Loaded CSV into database successfully"}
    except Exception as exc:
        return HTTPException(
            status_code=404,
            detail=f"Could not load CSV {exc!s}"
        )

@app.get("/records/")
def get_records_count(db: Session = Depends(get_db)):
    try:
        records = db.query(models.Customers).with_entities(func.count(models.Customers.rrn)).scalar()
        return {"number of records": records}
    except Exception as exc:
        return HTTPException(
            status_code=404,
            details=f"Couldn't read records {exc!s}"
        )

@app.get("/banks/")
def get_unique_banks(db: Session = Depends(get_db)):
    try:
        unique_banks = db.query(models.Customers.bank_name).distinct().count()
        return {"Number of Unique Banks": unique_banks}
    except Exception as exc:
        return HTTPException(
            status_code=404,
            details=f"Couldn't get banks list {exc!s}"
        )

@app.get("/transaction_count/{from_date}/{to_date}")
def get_transaction_count(from_date: str, to_date: str, db: Session = Depends(get_db)):
    try:
        from_date = (datetime.strptime(from_date, "%Y-%m-%d")).date()
        to_date = (datetime.strptime(to_date, "%Y-%m-%d")).date()
        records = db.query(models.Customers).filter(models.Customers.TXN_DATE.between(from_date,to_date)).count()
        return {f"Number of transaction between {from_date} and {to_date}": records}
    except Exception as exc:
        return HTTPException(
            status_code=404,
            details=f"error {exc!s}"
        )

@app.get("/customer_names/")
def get_customer_names(db: Session = Depends(get_db)):
    try:
        customers = db.query(models.Customers.acc_holder_name).all()
        return {"Customer names": customers}
    except Exception as exc:
        return HTTPException(
            status_code=404,
            details=f"Error fetching customer names {exc!s}"
        )

@app.get("/transaction_summary/")
def get_trans_summary(db: Session = Depends(get_db)):
    try:
        type_summary = db.query(models.Customers.txn_type, func.count(models.Customers.txn_type).label("Count")).group_by(models.Customers.txn_type).all()
        return {"Amount Summary on transaction type": type_summary}
    except Exception as exc:
        return HTTPException(
            status_code=404,
            details=f"Exception {exc!s}"
        )

@app.get("/transaction_amount_summary/")
def get_trans_amount_summary(db: Session = Depends(get_db)):
    try:
        type_summary = db.query(models.Customers.txn_type, func.sum(models.Customers.AMOUNT).label("AMOUNT")).group_by(models.Customers.txn_type).all()
        return {"Amount Summary on transaction type": type_summary}
    except Exception as exc:
        return HTTPException(
            status_code=404,
            details=f"Exception {exc!s}"
        )

@app.get("/total_transaction_amount/")
def get_total_trans_amount(db: Session = Depends(get_db)):
    try:
        type_summary = db.query(func.sum(models.Customers.AMOUNT).label("Total Amount")).all()
        return {"Amount Summary on transaction type": type_summary}
    except Exception as exc:
        return HTTPException(
            status_code=404,
            details=f"Exception {exc!s}"
        )
