from conexion import Conexion
from stand import Stand


def votarStand(conexion:Conexion, id_stand):
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
            SELECT id_stand, nombre, descripcion, curso, orientacion, profesor, votos FROM stands
            """)

            res = cursor.fetchall()
            stands = []
            for r in res:
                nStand = Stand(id_stand=r[0],
                            nombre=r[1], 
                            descripcion=r[2], 
                            curso=r[3],
                            orientacion=r[4],
                            profesor=r[5],
                            votos=res[6])
                
                stands.append(nStand)
            return stands
    except Exception as e:
        raise e


def buscarStand(conexion:Conexion, id_stand):
    try:
        with conexion.cursor() as cursor:
            cursor.execute("""
            SELECT id_stand, nombre, descripcion, curso, orientacion, profesor
            FROM stands WHERE id_stand = (%s)
            """, (id_stand,))
            res = cursor.fetchone()
            if res:
                stand = Stand(
                    id_stand=res[0],
                    nombre=res[1],
                    descripcion=res[2],
                    curso=res[3],
                    orientacion=res[4],
                    profesor=res[5]
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
            INSERT INTO stands(nombre, descripcion, curso, orientacion, profesor)
            VALUES(%s,%s,%s,%s,%s)""", 
            (stand.nombre, stand.descripcion, stand.curso, stand.orientacion, stand.profesor))

            conexion.commit()
    except Exception as e:
        conexion.rollback()
        raise e
