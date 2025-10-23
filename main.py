import datetime
from datetime import timedelta, datetime
from dotenv import load_dotenv
from fastapi import FastAPI, Response, Request
import os
from conexion import Conexion
from rep import*
from stand import Stand
load_dotenv()
var = os.getenv("DATABASE_URL")

conexion = Conexion(var)

dict = verStands(conexion)
#print(dict)
#stand = buscarStand(conexion, 1)
#print(stand)

app = FastAPI()

primer_stand = Stand(nombre="Flores", 
                     descripcion="Stand de Flores...",
                     year=2, 
                     division=2, 
                     orientacion="Ciclo Basico",
                     profesor="Yoyo")

"""cargarStand(conexion, primer_stand)
dict = verStands(conexion)
print(dict)"""

@app.get("/")
async def main():
    return {"Mensaje": "corriendose"}


@app.get("/stands")
async def stands():
    try:
        stands = verStands(conexion)
        return stands
    except Exception as e:
        return {"Error": str(e)}

@app.get("/stands/{stand_id}")
async def verStand(stand_id):
    try:
        stand = buscarStand(conexion, stand_id)
        if stand:
            return stand
        else:
            return {"Mensaje": "Stand inexistente"}
    except Exception as e:
        return {"Error": str(e)}

@app.post("/stands/{stand_id}/votar")
async def votar(stand_id, response:Response, request:Request):
    try:
        ya_voto = request.cookies.get('ya_voto')
        exp = datetime.now()
        exp1 = exp.replace(hour=8, minute=0, second=0, microsecond=0) + timedelta(days=1)

        if(ya_voto):
            return({
            "estado": False,
            "mensaje": "Ya voto, no puede volver a votar por hoy"
            })
        
        else:
            response.set_cookie(key="ya_voto", value=True, expires=exp1)
            votar(conexion, stand_id)
            return({
            "estado": True,
            "mensaje": "Voto sumado"
            })
    except Exception as e:
        return {"Error": str(e)}
    