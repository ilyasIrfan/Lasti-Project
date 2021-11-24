from os import write
import uvicorn
import json
from fastapi import FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

with open("ingredients_id1.json", "r") as read_file:
    data_bumbu_id1 = json.load(read_file)

with open("ingredients_id2.json", "r") as read_file:
    data_bumbu_id2 = json.load(read_file)

with open("ingredients_id3.json", "r") as read_file:
    data_bumbu_id3 = json.load(read_file)

with open("food.json", "r") as read_file:
    data_menu = json.load(read_file)

app = FastAPI()


@app.get("/")
def root():
    return ("Welcome to YamYam")


@app.get("/bumbu/{food_id}")
async def read_all_ingredients_food(food_id: int):
    if food_id == 1:
        return data_bumbu_id1
    elif food_id == 2:
        return data_bumbu_id2
    elif food_id == 3:
        return data_bumbu_id3
    else:
        return "Tidak ada id berupa " + str(food_id)


@app.get("/makanan")
async def read_all_food():
    return data_menu


@app.get("/bumbu/{food_id}/{bumbu_id}")
async def read_ingredient(food_id: int, bumbu_id: int):
    if food_id == 1:
        for kondimen_item in data_bumbu_id1['bumbu']:
            if kondimen_item['id'] == bumbu_id:
                return kondimen_item
        raise HTTPException(
            status_code=404, detail=f'data tidak ditemukan'
        )
    elif food_id == 2:
        for kondimen_item in data_bumbu_id2['bumbu']:
            if kondimen_item['id'] == bumbu_id:
                return kondimen_item
        raise HTTPException(
            status_code=404, detail=f'data tidak ditemukan'
        )
    elif food_id == 3:
        for kondimen_item in data_bumbu_id3['bumbu']:
            if kondimen_item['id'] == bumbu_id:
                return kondimen_item
        raise HTTPException(
            status_code=404, detail=f'data tidak ditemukan'
        )
    else:
        return "Tidak ada id berupa " + str(food_id)


@app.get("/makanan/{food_id}")
async def read_makanan(food_id: int):
    for food_item in data_menu['makanan']:
        if food_item['id'] == food_id:
            return food_item
    raise HTTPException(
        status_code=404,
        detail=f'data tidak ditemukan'
    )


@app.get("/ingredients_control/{food_id}/{bumbu_id}")
async def ingredients_control(food_id: int, bumbu_id: int, massa: int):
    return hitungSemuaMassaBumbu(food_id,  bumbu_id, massa)


@app.get("/food_control/{food_id}")
async def food_control(food_id: int, suhu: int, kelembaban: int):
    for food_item in data_menu['makanan']:
        if food_item['id'] == food_id:
            suhu_maks = food_item['suhuMax']
            suhu_min = food_item['suhuMin']
            kelembaban_maks = food_item['humidMax']
            kelembaban_min = food_item['humidMin']

    if check_temperature(suhu, suhu_min, suhu_maks) and check_humidity(kelembaban, kelembaban_min, kelembaban_maks):
        return "makanan sudah siap disajikan!"
    elif check_temperature(suhu, suhu_min, suhu_maks) and not(check_humidity(kelembaban, kelembaban_min, kelembaban_maks)):
        return recommend_humidity(kelembaban, kelembaban_min, kelembaban_maks)
    elif not(check_temperature(suhu, suhu_min, suhu_maks)) and check_humidity(kelembaban, kelembaban_min, kelembaban_maks):
        return recommend_temperature(suhu, suhu_min, suhu_maks)
    else:
        return recommend_all(suhu, suhu_min, suhu_maks, kelembaban, kelembaban_min, kelembaban_maks)


def check_temperature(suhu_makanan: int, suhu_min: int, suhu_maks: int):
    good_temperature = False
    if((suhu_makanan >= suhu_min) and (suhu_makanan <= suhu_maks)):
        good_temperature = True
    return good_temperature


def check_humidity(kelembaban_makanan: int, kelembaban_min: int, kelembaban_maks: int):
    good_humidity = False
    if((kelembaban_makanan >= kelembaban_min) and (kelembaban_makanan <= kelembaban_maks)):
        good_humidity = True
    return good_humidity


def recommend_temperature(suhu_makanan: int, suhu_min: int, suhu_maks: int):
    if(suhu_makanan > suhu_maks):
        return "suhu terlalu tinggi, kurangi suhu setidaknya " + str(suhu_makanan-suhu_maks) + "°C"
    elif(suhu_makanan < suhu_min):
        return "suhu terlalu rendah, tambahi suhu setidaknya " + str(suhu_min-suhu_makanan) + "°C"


def recommend_humidity(kelembaban_makanan: int, kelembaban_min: int, kelembaban_maks: int):
    if(kelembaban_makanan > kelembaban_maks):
        return "kelembaban terlalu tinggi, kurangi kelembaban setidaknya " + str(kelembaban_makanan-kelembaban_maks) + "%RH"
    elif(kelembaban_makanan < kelembaban_min):
        return "kelembaban terlalu rendah, tambahi kelembaban setidaknya " + str(kelembaban_min-kelembaban_makanan) + "%RH"


def recommend_all(suhu_makanan: int, suhu_min: int, suhu_maks: int, kelembaban_makanan: int, kelembaban_min: int, kelembaban_maks: int):
    return recommend_temperature(suhu_makanan, suhu_min, suhu_maks) + ". Kemudian, " + recommend_humidity(kelembaban_makanan, kelembaban_min, kelembaban_maks)


def hitungSemuaMassaBumbu(food_id, bumbu_id, massa):
    if food_id == 1:
        if massa > data_bumbu_id1["bumbu"][bumbu_id-1]["massa"]:
            return "massa berlebih, kurangi " + str(massa - data_bumbu_id1["bumbu"][bumbu_id-1]["massa"]) + " gram!"
        elif massa < data_bumbu_id1["bumbu"][bumbu_id-1]["massa"]:
            return "massa kurang, tambahkan " + str(data_bumbu_id1["bumbu"][bumbu_id-1]["massa"] - massa) + " gram!"
        else:
            return "massa sudah sesuai, lanjut ke proses selanjutnya!"
    elif food_id == 2:
        if massa > data_bumbu_id2["bumbu"][bumbu_id-1]["massa"]:
            return "massa berlebih, kurangi " + str(massa - data_bumbu_id2["bumbu"][bumbu_id-1]["massa"] - massa) + " gram!"
        elif massa < data_bumbu_id2["bumbu"][bumbu_id-1]["massa"]:
            return "massa kurang, tambahkan " + str(data_bumbu_id2["bumbu"][bumbu_id-1]["massa"] - massa) + " gram!"
        else:
            return "massa sudah sesuai, lanjut ke proses selanjutnya!"
    elif food_id == 3:
        if massa > data_bumbu_id3["bumbu"][bumbu_id-1]["massa"]:
            return "massa berlebih, kurangi " + str(massa - data_bumbu_id3["bumbu"][bumbu_id-1]["massa"] - massa) + " gram!"
        elif massa < data_bumbu_id3["bumbu"][bumbu_id-1]["massa"]:
            return "massa kurang, tambahkan " + str(data_bumbu_id3["bumbu"][bumbu_id-1]["massa"] - massa) + " gram!"
        else:
            return "massa sudah sesuai, lanjut ke proses selanjutnya!"
