from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import psycopg2
import os

app = FastAPI()
templates = Jinja2Templates(directory=os.path.dirname(os.path.abspath(__file__)))

conn = psycopg2.connect(
    dbname="testMTS",
    user="ivanz",
    host="localhost",
    port="5432"
)


# Маршрут для отображения HTML страницы
@app.get("/")
async def read_item(request: Request):
    return templates.TemplateResponse("homepage.html", {"request": request})


# Маршрут для поиска данных в таблице по выбранному столбцу
@app.get("/search_by_column")
async def search_trip_by_column(request: Request, search_value: str, column: str):
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM trip where {column} = '{search_value}'")
    rows = cur.fetchall()
    cur.close()
    return templates.TemplateResponse("homepage.html", {"request": request, "results": rows})


# Маршрут для получения данных из базы данных
# @app.get("/get_data/{plane}")
# async def get_data(plane: str):
#     cur = conn.cursor()
#     cur.execute(f"SELECT * FROM trip where plane= '{plane}'")
#     rows = cur.fetchall()
#     cur.close()
#     return rows
