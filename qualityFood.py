from os import write
import uvicorn
import json
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

with open("ingredients.json","r") as read_file:
	data_bumbu = json.load(read_file)

with open("food.json","r") as read_file:
	data_menu = json.load(read_file)

app = FastAPI() 

@app.get("/")
def root():
	return ("Welcome to YamYam")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)