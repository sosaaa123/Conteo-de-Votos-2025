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
load_dotenv()
var = os.getenv("DATABASE_URL")

conexion = Conexion(var)

dict = verStands(conexion)
#print(dict)
#stand = buscarStand(conexion, 1)
#print(stand)

cur = conexion.cursor()

origenes = ["http://localhost:5173", "https://front-votos.vercel.app"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = origenes,
    allow_methods = ["*"],
    allow_credentials = True, 
    allow_headers = ["*"],
)

"""primer_stand = Stand(nombre="Fweesdds", 
                     descripcion="tweeasasnd de Fslores...",
                     curso="4to 5ta", 
                     orientacion="Cicsdaassico",
                     profesor="oa")
"""

def horarios(fecha: datetime):
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

stands_prueba = [
    Stand(
        nombre="Robótica Educativa",
        descripcion="Demostración de robots programados por estudiantes",
        curso="4to Año",
        orientacion="Informática",
        profesor="María González",
        materia="Tecnología"
    ),
    Stand(
        nombre="Química Divertida",
        descripcion="Experimentos químicos interactivos y seguros",
        curso="5to Año",
        orientacion="Ciencias Naturales",
        profesor="Carlos Rodríguez",
        materia="Química"
    ),
    Stand(
        nombre="Historia Viva",
        descripcion="Recreación de eventos históricos con maquetas",
        curso="3ro Año",
        orientacion="Ciencias Sociales",
        profesor="Ana Martínez",
        materia="Historia"
    ),
    Stand(
        nombre="Matemática Recreativa",
        descripcion="Juegos y acertijos matemáticos para todas las edades",
        curso="2do Año",
        orientacion="Economía",
        profesor="Luis Fernández",
        materia="Matemática"
    ),
    Stand(
        nombre="Arte Digital",
        descripcion="Exposición de obras creadas con herramientas digitales",
        curso="6to Año",
        orientacion="Arte",
        profesor="Laura Díaz",
        materia="Educación Artística"
    ),
    Stand(
        nombre="Biología Molecular",
        descripcion="Demostraciones de ADN y células con microscopios",
        curso="5to Año",
        orientacion="Biología",
        profesor="Roberto Silva",
        materia="Biología"
    ),
    Stand(
        nombre="Programación de Videojuegos",
        descripcion="Juegos simples creados por estudiantes en Python",
        curso="4to Año",
        orientacion="Informática",
        profesor="Patricia López",
        materia="Programación"
    )]


for stand in stands_prueba:
    cargarStand(conexion, stand)


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
        if not (horarios(exp)):
            return({
                "estado": False,
                "mensaje": "No se puede votar, fuera de horario"
            })

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
    
