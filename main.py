import datetime
from datetime import time, timedelta, datetime
import uuid
from dotenv import load_dotenv
from fastapi import Cookie, FastAPI, Response, Request
import os
from conexion import Conexion
from rep import*
from stand import Stand
from fastapi.middleware.cors import CORSMiddleware
import pytz
load_dotenv()
var = os.getenv("DATABASE_URL")

conexion = Conexion(var)

dict = verStands(conexion)
#print(dict)
#stand = buscarStand(conexion, 1)
#print(stand)

arg = pytz.timezone('America/Argentina/Buenos_Aires')

cur = conexion.cursor()

origenes = ["http://localhost:5173", "https://front-votos.vercel.app", "https://dashboard-votos-skea.vercel.app/"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = origenes,
    allow_methods = ["*"],
    allow_credentials = True, 
    allow_headers = ["*"],
)

primer_stand = Stand(nombre="Impresion 3D", 
                     descripcion="Se demostrara las habilidades en diseño 3D y codificacion G aprendidas en el año",
                     curso="6º 2da", 
                     orientacion="Electromecanica",
                     profesor="Anderson, Facundo; Sein, Martín",
                     materia="Electromecanica materia")

segundo_stand = Stand

def horarios(fecha: datetime):
    fecha = arg.localize(fecha)
    hora_actual = fecha.time()

    horarios = [
        (time(8, 0), time(12, 0)),
        (time(13, 0), time(17, 30)),
        (time(17, 40), time(21, 0)),
    ]

    for inicio, fin in horarios:
        if inicio <= hora_actual <= fin:
            return True

    return False

"""
if not (horarios(exp)):
            return({
                "estado": False,
                "mensaje": "No se puede votar, fuera de horario"
            })

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
        exp = arg.localize(datetime.now())
        exp1 = exp.replace(hour=8, minute=0, second=0, microsecond=0) + timedelta(days=1)
        dia = exp1.day
        mes = exp1.month

        if(votante_id):
            return({
            "estado": False,
            "mensaje": f"Ya uso su voto diario, vuelva mañana {f"{dia}/{mes}"}.",
            "ya_voto": True
            })

        """"""  """y reemplazarlo por age"""
        response.set_cookie(
            key="votante_id",
            value=str(uuid.uuid4()),
            httponly=True,
            expires=exp1,
            path="/",
            samesite="none",
            secure=True       
        )
        votarStand(conexion, stand_id)

        return({
            "estado": True,
            "mensaje": f"¡Muchas gracias por su voto!"
        })
    except Exception as e:
        return {"Error": str(e)}
    
print(horarios(datetime.now()))
exp = arg.localize(datetime.now())
exp1 = exp.replace(hour=8, minute=0, second=0, microsecond=0) + timedelta(days=1)
print(exp1)