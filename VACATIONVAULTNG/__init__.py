from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="VacationVaultNG API",
    version="1.0.0"
)

# List of allowed origins
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

from VACATIONVAULTNG import models
from database import engine
models.Base.metadata.create_all(bind=engine)

from VACATIONVAULTNG import (routes)
# from SECURITY import (pydantic_models, helper)
