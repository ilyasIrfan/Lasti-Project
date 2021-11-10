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

@app.get("/kondimen")
async def read_all_kondimens():
	return data_bumbu

@app.get("/makanan")
async def read_all_food():
	return data_menu

@app.get("/kondimen/{kondimen_id}")
async def read_kondimen(kondimen_id : int):
	for kondimen_item in data_bumbu['kondimen']:
		if kondimen_item['id'] == kondimen_id:
			return kondimen_item
	raise HTTPException(
			status_code = 404,
			detail = f'data tidak ditemukan'
		)

@app.get("/makanan/{food_id}")
async def read_kondimen(food_id : int):
	for food_item in data_menu['makanan']:
		if food_item['id'] == food_id:
			return food_item
	raise HTTPException(
			status_code = 404,
			detail = f'data tidak ditemukan'
		)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)