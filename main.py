import datetime
from datetime import timedelta, datetime
import uuid
from dotenv import load_dotenv
from fastapi import Cookie, FastAPI, Response, Request
import os
from conexion import Conexion
from rep import*
from stand import Stand
from fastapi.middleware.cors import CORSMiddleware
load_dotenv()
var = os.getenv("DATABASE_URL")

conexion = Conexion(var)

dict = verStands(conexion)
#print(dict)
#stand = buscarStand(conexion, 1)
#print(stand)



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:5173"],
    allow_methods = ["*"],
    allow_credentials = True, 
    allow_headers = ["*"],
)

"""primer_stand = Stand(nombre="Fweesdds", 
                     descripcion="tweeasasnd de Fslores...",
                     curso="4to 5ta", 
                     orientacion="Cicsdaassico",
                     profesor="oa")

cargarStand(conexion, primer_stand)

dict = verStands(conexion)
print(dict)

st = buscarStand(conexion, 1)
print(st)
"""

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

@app.get("/stands/{stand_id}/votar")
async def votar(stand_id, response:Response, votante_id:str=Cookie(None)):
    try:
        exp = datetime.now()
        exp1 = exp.replace(hour=8, minute=0, second=0, microsecond=0) + timedelta(days=1)

        if(votante_id):
            return({
            "estado": False,
            "mensaje": "Ya voto, no puede volver a votar por hoy"
            })

        response.set_cookie(
            key="votante_id",
            value=str(uuid.uuid4()),
            httponly=True,
            max_age=60,
            path="/",
            samesite="none",
            secure=True       
        )
        votarStand(conexion, stand_id)

        return({
            "estado": True,
            "mensaje": "Se ha completado un voto"
        })
    except Exception as e:
        return {"Error": str(e)}
    
