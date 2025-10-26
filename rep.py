from conexion import Conexion
from stand import Stand


def votar(conexion:Conexion, id_stand):
    try:
        with conexion.cursor() as cursor:
            cursor.execute("""
            UPDATE stands
            SET votos = votos + 1
            WHERE id_stand = (%s)
            """,(id_stand,))
            conexion.commit()
            
    except Exception  as e:
        conexion.rollback()
        raise e
    
def verStands(conexion:Conexion):
    try:
        with conexion.cursor() as cursor:
            cursor.execute("""
            SELECT id_stand, nombre, descripcion, año, division, orientacion, profesor, votos FROM stands
            """)

            res = cursor.fetchall()
            stands = []
            for r in res:
                nStand = Stand(id_stand=r[0],
                            nombre=r[1], 
                            descripcion=r[2], 
                            year=r[3], 
                            division=r[4], 
                            orientacion=r[5],
                            profesor=r[6],
                            votos=r[7])
                
                stands.append(nStand)
            return stands
    except Exception as e:
        raise e


def buscarStand(conexion:Conexion, id_stand):
    try:
        with conexion.cursor() as cursor:
            cursor.execute("""
            SELECT id_stand, nombre, descripcion, año, division, orientacion, profesor, votos
            FROM stands WHERE id_stand = (%s)
            """, (id_stand,))
            res = cursor.fetchone()
            if res:
                stand = Stand(
                    id_stand=res[0],
                    nombre=res[1],
                    descripcion=res[2],
                    year=res[3],
                    division=res[4],
                    orientacion=res[5],
                    profesor=res[6],
                    votos=res[7]
                )

                return stand
            else:
                return None
    except Exception as e:
        raise e



def cargarStand(conexion:Conexion, stand:Stand):
    try:
        with conexion.cursor() as cursor:
            cursor.execute("""
            INSERT INTO stands(nombre, descripcion, año, division, orientacion, profesor)
            VALUES(%s,%s,%s,%s,%s,%s)""", 
            (stand.nombre, stand.descripcion, stand.year, stand.division, stand.orientacion, stand.profesor))

            conexion.commit()
    except Exception as e:
        conexion.rollback()
        raise e
