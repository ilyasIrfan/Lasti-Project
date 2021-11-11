from os import write
import uvicorn
import json
from fastapi import FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

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

@app.get("/ingredients_control")
async def ingredients_control(food_id : int, jumlah_buat : int):
    if jumlah_buat < 10:
        return "Minimal pembuatan perbatch harus sebanyak 10 porsi"
    else:
        return hitungSemuaMassaBumbu(food_id, jumlah_buat)

@app.get("/food_control")
async def food_control(suhu : int, kelembaban : int):
    if suhu < 35:
        return "harus dipanaskan!"
    elif suhu > 50:
        return "suhu terlalu tinggi, perlu didiamkan sebentar!"
    else: 
        return "makanan sudah siap disajikan!"

def hitungSemuaMassaBumbu(id,jumlah):
	if id == 1:
		return {
				"jumlah " + data_bumbu["kondimen"][0]["name"] + " yang harus disiapkan": str(data_bumbu["kondimen"][0]["massa"]*jumlah) + " gram" ,
				"jumlah " + data_bumbu["kondimen"][1]["name"] + " yang harus disiapkan": str(data_bumbu["kondimen"][1]["massa"]*jumlah) + " gram" ,
				"jumlah " + data_bumbu["kondimen"][2]["name"] + " yang harus disiapkan": str(data_bumbu["kondimen"][2]["massa"]*jumlah) + " gram" ,
				"jumlah " + data_bumbu["kondimen"][3]["name"] + " yang harus disiapkan": str(data_bumbu["kondimen"][3]["massa"]*jumlah) + " gram" ,
				"jumlah " + data_bumbu["kondimen"][8]["name"] + " yang harus disiapkan": str(data_bumbu["kondimen"][8]["massa"]*jumlah) + " gram" ,
				"jumlah " + data_bumbu["kondimen"][9]["name"] + " yang harus disiapkan": str(data_bumbu["kondimen"][9]["massa"]*jumlah) + " gram"  
		}
	else:
		return {
				"jumlah " + data_bumbu["kondimen"][0]["name"] + " yang harus disiapkan": str(data_bumbu["kondimen"][0]["massa"]*jumlah) + " gram" ,
				"jumlah " + data_bumbu["kondimen"][1]["name"] + " yang harus disiapkan": str(data_bumbu["kondimen"][1]["massa"]*jumlah) + " gram" ,
				"jumlah " + data_bumbu["kondimen"][2]["name"] + " yang harus disiapkan": str(data_bumbu["kondimen"][2]["massa"]*jumlah) + " gram" ,
				"jumlah " + data_bumbu["kondimen"][3]["name"] + " yang harus disiapkan": str(data_bumbu["kondimen"][3]["massa"]*jumlah) + " gram" ,
				"jumlah " + data_bumbu["kondimen"][4]["name"] + " yang harus disiapkan": str(data_bumbu["kondimen"][4]["massa"]*jumlah) + " gram" ,
				"jumlah " + data_bumbu["kondimen"][5]["name"] + " yang harus disiapkan": str(data_bumbu["kondimen"][5]["massa"]*jumlah) + " gram" ,
				"jumlah " + data_bumbu["kondimen"][6]["name"] + " yang harus disiapkan": str(data_bumbu["kondimen"][6]["massa"]*jumlah) + " gram" ,  
				"jumlah " + data_bumbu["kondimen"][7]["name"] + " yang harus disiapkan": str(data_bumbu["kondimen"][7]["massa"]*jumlah) + " gram" ,  
				"jumlah " + data_bumbu["kondimen"][8]["name"] + " yang harus disiapkan": str(data_bumbu["kondimen"][8]["massa"]*jumlah) + " gram" ,  
				"jumlah " + data_bumbu["kondimen"][9]["name"] + " yang harus disiapkan": str(data_bumbu["kondimen"][9]["massa"]*jumlah) + " gram" ,  
				"jumlah " + data_bumbu["kondimen"][10]["name"] + " yang harus disiapkan": str(data_bumbu["kondimen"][10]["massa"]*jumlah) + " gram"   
		}
	
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)