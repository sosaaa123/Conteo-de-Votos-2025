import os
from dotenv import load_dotenv
import qrcode
from conexion import Conexion
url="http://localhost:5173/stand/4"
img = qrcode.make(url)
img.save("qr.png")
load_dotenv()
var = os.getenv("DATABASE_URL")

conexion = Conexion(var)
def qrs(conexion:Conexion):
    try:
        with conexion.cursor() as cursor:
            cursor.execute("""
            SELECT id_stand, nombre FROM stands
            """)

            res = cursor.fetchall()
            return res
    except Exception as e:
        raise e

#print(qrs(conexion))

"""For i in range(6):
    url = f"http://localhost:5173/stand/{i+9}"
    img.save(f"qr{i+9}.png")"""