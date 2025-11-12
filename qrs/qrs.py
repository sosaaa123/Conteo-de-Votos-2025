import os
from dotenv import load_dotenv
import qrcode
from conexion import Conexion
url="https://front-votos.vercel.app/stand/153"
img = qrcode.make(url)
img.save("dioses.png")
load_dotenv()
var = os.getenv("DATABASE_URL")

"""conexion = Conexion(var)
cursor = conexion.cursor()
res = []
try:
    with conexion.cursor() as cursor:
        
        cursor.execute("
        SELECT id_stand, nombre, curso FROM stands")
        res = cursor.fetchall()
        for i in res:
            url=f"https://front-votos.vercel.app/stand/{i[0]}"
            img = qrcode.make(url)
            if "¿" in i[1]:
                rp =  i[1].replace("¿", "").replace(" ", "_").replace("?", "")
                img.save(f"{rp}___{i[2]}.png")
            else:
                img.save(f"{i[1]}___{i[2]}.png")

except Exception as e:
    raise e

"""

#print(qrs(conexion))

"""For i in range(6):
    url = f"http://localhost:5173/stand/{i+9}"
    img.save(f"qr{i+9}.png")"""