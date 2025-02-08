from pymongo import MongoClient # type: ignore
import pickle
import json
import os

def conexion_bd():
    """
    Establece una conexión con una base de datos MongoDB utilizando credenciales almacenadas en variables de entorno.

    Returns:
        MongoClient: Cliente de conexión a MongoDB si se establece correctamente.

    Raises:
        Exception: Si ocurre un error durante la conexión.
    """

    db_password = os.getenv("mongo_password") 
    uri = f"mongodb+srv://root:{db_password}@cluster0.jqyt6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(uri)

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return client
        
    except Exception as e:
        print(f"Error al conectarse a la base de datos: {e}")

def borrar_bbdd(nombre_bbdd):
    try:
        client = conexion_bd()
        client.list_database_names()
        client.drop_database(nombre_bbdd)
        client.list_database_names()
    except:
        print("Error al borrar la base de datos")


def cargar_datos_mongo():
    """
    Carga datos JSON desde archivos locales en las colecciones 'linkedin' e 'infojobs' de MongoDB.

    Este método busca archivos JSON en el directorio `data/skills_filtradas_relevantes/` y los inserta
    en las colecciones correspondientes según el nombre del archivo.

    Raises:
        Exception: Si ocurre un error durante la inserción de los datos.
    """

    client = conexion_bd()

    if client:
        db = client['db_empleatech_v2']
        collection_linkedin = db['linkedin']
        collection_infojobs = db['infojobs']


        path_skills_filtradas = "data/skills_filtradas_relevantes/"
        files_offers = os.listdir(path_skills_filtradas)

        try:
            for file in files_offers:

                nombre_file = path_skills_filtradas + file

                with open(f'{nombre_file}', 'r', encoding='utf-8') as archivo:
                        json_datos = json.load(archivo)

                if 'linkedin' in file:
                    print(f"Insertando file: {file}")
                    collection_linkedin.insert_many(json_datos)

                if 'infojobs' in file:
                    print(f"Insertando file: {file}")
                    collection_infojobs.insert_many(json_datos)
            
            print("---- Insercion en la base de datos finalizada ----\n")

        except Exception as e:
            print(f"Ha ocurrido un error durante la insercion: {e}")

def cargar_skills_mongo():
    """
    Inserta las listas de habilidades técnicas en MongoDB desde un archivo Pickle.
    """

    client = conexion_bd()

    if client:

        # Lista de las skills sin categorizar
        # db = client['db_empleatech_v2']
        # collection = db['hard_skills']

        # try:
        #     file_path = "data/lista_hard_skills.pkl"
        #     with open(file_path, 'rb') as file:
        #         lista_hard_skills = pickle.load(file)
        #     documento = {"lista_skills": lista_hard_skills}
 
        #     collection.insert_one(documento)

        #     #print("Skills sin categorizar insertadas en la base de datos correctamente.")
                
        # except Exception as e:
        #     print(f"Ha ocurrido un error durante la insercion: {e}")


        # Lista de las skills categorizadas
        db = client['db_empleatech_v2']
        collection = db['hard_skills_categorizadas']

        try:
            file_path = "data/diccionario_skills_categorizadas.pkl"
            with open(file_path, 'rb') as file:
                diccionario_skills_categorizadas = pickle.load(file)
            documento = {"diccionario_skills_categorizadas": diccionario_skills_categorizadas}
 
            collection.insert_one(documento)

            print("Skills categorizadas insertadas en la base de datos correctamente.")
                
        except Exception as e:
            print(f"Ha ocurrido un error durante la insercion: {e}")


def obtener_todos_los_datos():
    """
    Recupera todos los documentos de las colecciones 'linkedin' e 'infojobs' en MongoDB.

    Returns:
        dict: Un diccionario con dos claves:
            - 'linkedin': Lista de documentos de la colección 'linkedin'.
            - 'infojobs': Lista de documentos de la colección 'infojobs'.
        None: Si ocurre un error al conectar o al obtener los datos.

    Raises:
        Exception: Si ocurre un error durante la conexión o recuperación de datos.
    """

    client = conexion_bd()

    try:
        db = client['db_empleatech_v2']
        
        collection_linkedin = db['linkedin']
        collection_infojobs = db['infojobs']
        collection_skills = db['hard_skills']
        collection_skills_categorizadas = db['hard_skills_categorizadas']

        # Obtener todos los documentos de las colecciones
        datos_linkedin = list(collection_linkedin.find())
        datos_infojobs = list(collection_infojobs.find())
        datos_skills = list(collection_skills.find())
        datos_skills_categorizadas = list(collection_skills_categorizadas.find())

        # Convertir ObjectId a string para facilitar el manejo
        for doc in datos_linkedin:
            doc['_id'] = str(doc['_id'])
        for doc in datos_infojobs:
            doc['_id'] = str(doc['_id'])

        print("Datos obtenidos de MongoDB correctamente.")

        return {
            "linkedin": datos_linkedin,
            "infojobs": datos_infojobs,
            "skills": datos_skills[0]['lista_skills'],
            "skills_categorizadas": datos_skills_categorizadas[0]["diccionario_skills_categorizadas"]
        }

    except Exception as e:
        print(f"Error al conectarse o al obtener los datos: {e}")
        return None