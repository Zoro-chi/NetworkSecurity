import sys, os
import certifi
import pymongo
import pandas as pd
from dotenv import load_dotenv

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from uvicorn import run as app_run
from starlette.responses import RedirectResponse

from network_security.logging.logger import logging
from network_security.exception.exception import NetworkSecurityException
from network_security.pipeline.training_pipeline import TrainingPipeline
from network_security.utils.common import load_object
from network_security.utils.ml_utils.model.estimator import NetworkModel
from network_security.constants.training_pipeline import (
    DATA_INGESTION_COLLECTION_NAME,
    DATA_INGESTION_DATABASE_NAME,
)

# Certifi is a carefully curated collection of Root Certificates for validating the trustworthiness of SSL certificates while verifying the identity of TLS hosts.
certificate_authority = certifi.where()

# Load the environment variables from the .env file
load_dotenv()


MONGODB_URI = os.getenv("MONGODB_URI")

# Connect to the MongoDB database
client = pymongo.MongoClient(MONGODB_URI, tlsCAFile=certificate_authority)
database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

# Create a FastAPI instance
app = FastAPI()
origins = ["*"]

# Add CORS middleware to the FastAPI instance
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the templates for the FastAPI instance
templates = Jinja2Templates(directory="./templates")


@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")


@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response(content="Training Pipeline Completed")
    except Exception as e:
        raise NetworkSecurityException(e, sys)


@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
        preprocessor = load_object("final_model/preprocessor.pkl")
        final_model = load_object("final_model/model.pkl")
        network_model = NetworkModel(preprocessor, final_model)
        print(df.iloc[0])
        y_pred = network_model.predict(df)
        print(y_pred)
        df["predicted_values"] = y_pred
        print(df["predicted_values"])
        # df["predicted_values"].replace(-1, 0)
        # return df.to_json()
        df.to_csv("prediction_output/predicted_values.csv")
        table_html = df.to_html(classes="table table-striped")
        return templates.TemplateResponse(
            "table.html",
            {
                "request": request,
                "table": table_html,
            },
        )
    except Exception as e:
        raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    # for dev - localhost
    # fro pro - 0.0.0.0
    app_run(app, host="localhost", port=8000)
