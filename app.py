import uvicorn
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from mobiles_dm import Mobile, Mobile_pd
from joblib import load
import pandas as pd
from copy import deepcopy

from pydantic import BaseModel
from sqlalchemy import create_engine, MetaData, Table, desc, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select

# API Initialization
app = FastAPI(
    title="Mobile Price Range Predictor - API",
    description="This API allows you to predict the price range based on a set of features",
    version="1.0.0",
)

# Data base connection
SQLALCHEMY_DATABASE_URL = "sqlite:///./base.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
metadata = MetaData()

# Sqlalchemy Session
SQLAchmSession = sessionmaker(bind=engine)

# db_ok stores the initial state of the database connection
try:
    mobile_pd_itm = Table("data_entered_pd", metadata, autoload_with=engine)
    db_ok = True
except:
    db_ok = False

# Loading pipeline for preprocessing and ML model pre-trained
classifier = load("./src/Pipelines/prange_ml_pipeline.joblib")

@app.get('/')
def index():
    return {'message': 'Go to /docs to view documentation'}

@app.post('/predict')
def predict_mobile_price_range(data:list[Mobile]) -> Mobile_pd:
    """Performs prediction on a data set in JSON format"""
    df_data = pd.DataFrame([d.model_dump() for d in data])
    
    # Applying the pre-processing and prediction pipeline
    prediction = classifier.predict(df_data)
    
    df_data_pd = deepcopy(df_data)
    df_data_pd['price_range_prediction'] = prediction
    mapping = {0:'Low', 1:'Mid', 2:'High', 3:'Very High'}
    df_data_pd['price_range_prediction'] = df_data_pd['price_range_prediction'].map(mapping)

    df_data_pd.to_sql('data_entered_pd', engine, if_exists='append', index=False)

    return JSONResponse(content=df_data_pd.to_json(orient='records'))
 
@app.get("/healthcheck")
def healthcheck():
    """Check API Health"""
    return True

@app.get("/healthcheckdatabase")
def healthcheckdatabase():
    """Allows you to know the current state of the database"""
    with SQLAchmSession() as session:
        query = select(mobile_pd_itm)
        data = session.execute(query)
    if not db_ok or data is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Inaccessible table or database")
    return {'Tabla accesible'}
    
@app.get("/getlastitem")
def getlastitem():
    """Returns the last entered data and its corresponding prediction"""
    with SQLAchmSession() as session:
        query = select(mobile_pd_itm).order_by(desc(mobile_pd_itm.c.id))
        item = session.execute(query).first()
        if item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Error: Empty Table")
        return item._mapping