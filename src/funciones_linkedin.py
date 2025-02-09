# Librerías de extracción de datos
# -----------------------------------------------------------------------
from bs4 import BeautifulSoup # type: ignore
import requests
import numpy as np # type: ignore
import json
import html
from tqdm import tqdm # type: ignore
from random import uniform
import os


# Tratamiento de datos
# -----------------------------------------------------------------------
import pandas as pd # type: ignore
from time import sleep

def carga_csv(local_path):
    df = pd.read_csv(local_path)
    return df


def elminacio_cabeceras_datos_invalidos(df):
    # Eliminamos las cabeceras
    filtro_cabecera = (df["job_title"] == "job_title") & (df["job_detail_url"] == "job_detail_url")
    df_v2 = df[~filtro_cabecera]

    # Eliminamos datos invalidos
    filtro_not_found = df_v2.isin(["not-found"]).any(axis=1)
    df_limpio = df_v2[~filtro_not_found].copy()
    df_limpio.reset_index(drop=True, inplace=True)
    
    return df_limpio

def check_fecha_correcta(df):

    df["job_listed_split"] = df["job_listed"].str.split()
    listas_validas = df["job_listed_split"].apply(lambda x: len(x) == 3)

    # Comprobar si todas las filas tienen tres elementos
    todas_validas = listas_validas.all()
    return todas_validas

def ordenar_datos_por_fecha(df):

    # Comprobamos que todas las fechas tienen en el mismo formato
    if check_fecha_correcta(df) == False:
        print("Las fechas no tienen un mismo formato")
        return df
    
    df_ordenado = df.copy()
    df_ordenado["X"] = df_ordenado["job_listed_split"].apply(lambda x: x[0]) # Columna que indica el NÚMERO de días, semanas, meses o años
    df_ordenado["Y"] = df_ordenado["job_listed_split"].apply(lambda x: x[1]) # Columna que indica el si son días, semanas, meses o años
    df_ordenado["Z"] = df_ordenado["job_listed_split"].apply(lambda x: x[2]) # Columna en la que comprobamos que solo este el valor "ago"

    if df_ordenado[df_ordenado["Z"]!="ago"].shape[0] != 0:
        print("Error en el formato de la fecha")
        return df

    # Eliminamos las ofertas de hace un año
    ofertas_year_ago = df_ordenado["Y"]=="year"
    df_ordenado = df_ordenado[~ofertas_year_ago].copy()
    df_ordenado.reset_index(drop=True, inplace=True)

    # Reemplazar plurales con sus equivalentes singulares
    plurals_to_singular = {"weeks": "week", "months": "month", "days": "day", "hours": "hour", "minutes":"minute"}
    df_ordenado["Y"] = df_ordenado["Y"].replace(plurals_to_singular)

    df_ordenado["X"] = pd.to_numeric(df_ordenado["X"], errors="coerce")


    # Ordanamos las ofertas de la más a la menos reciente
    orden_personalizado = {"minute": 0, "hour": 1, "day": 2, "week": 3, "month": 4, "year": 5}

    # Agregar una columna temporal para mapear el orden personalizado
    df_ordenado["orden"] = df_ordenado["Y"].map(orden_personalizado)
    df_ordenado_final = df_ordenado.sort_values(by=["orden", "X"], ascending=[True, True])
    df_ordenado_final = df_ordenado_final.drop(columns=["orden", "X", "Y", "Z", "job_listed_split"])
    df_ordenado_final = df_ordenado_final.reset_index(drop=True)

    return df_ordenado_final

def limpieza_completa():
    empleos = ["data_science", "data_analyst", "data_engineer"]

    file_path = f"data/datos_links_limpios"
    absolute_path = os.path.abspath(file_path)

    if not os.path.exists(absolute_path):
        os.makedirs(absolute_path)

    for empleo in empleos:
        print(f"Links de {empleo.upper()}:")

        # Carga de datos
        df = carga_csv(f"linkedin/data/linkedin_madrid_{empleo}.csv")
        print(f"\n   >> Cargado correctamente el df con dimensiones: {df.shape}")

        # Limpieza de cabeceras y datos erroneos
        df_limpio = elminacio_cabeceras_datos_invalidos(df)
        print(f"\n   >> Tras la elminación de cabeceras y datos errónes el shape es de: {df_limpio.shape}")

        # Ordenamos las ofertas por fecha de publicaciónde más a menos reciente
        print("\n   >> Ordenamos las ofertas por fecha de publicación de más a menos reciente y eliminamos las ofertas de más de un año:")
        df_ordenado = ordenar_datos_por_fecha(df_limpio)

        # Almacenamos los datos
        df_ordenado.to_csv(f"data/datos_links_limpios/linkedin_links_{empleo}.csv")
        print(f"\n   >> Datos almacenados en data/datos_links_limpios/linkedin_links_{empleo}.csv")

        print("\n=========================================================================================================================\n")


def get_full_linkedin_data():

    #empleos = ["data_science", "data_analyst", "data_engineer"]
    empleos = ["data_engineer"]

    # Creamos la carpeta donde se van a guardar los resultados si no existe
    file_path = f"data/datos_descripcion_ofertas"
    absolute_path = os.path.abspath(file_path)

    if not os.path.exists(absolute_path):
        os.makedirs(absolute_path)

    # Iteramos por cada empleo
    for empleo in empleos:

        print(f"Links de {empleo.upper()}:")
        
        df = pd.read_csv(f"data/datos_links_limpios/linkedin_links_{empleo}.csv", index_col=0)
        df_jobs = pd.DataFrame()
        jobs_exceeded_time = 0

        for i in tqdm(range(df.shape[0])):
            print("------------------------------------------------")
            tries = 1
            url = df.loc[i, "job_detail_url"]
            
            while tries <= 10:
                try:
                    res = requests.get(url, timeout=30)  # Establecemos un tiempo de espera
                    status_code = res.status_code
                    if status_code == 200:
                        break  # Salimos del bucle si obtenemos un código 200
                    
                except requests.exceptions.Timeout:
                    print(f"Timeout en intento {tries} para {url}")
                except requests.exceptions.RequestException as e:
                    print(f"Error en intento {tries} para {url}: {e}")
                
                tries += 1
                sleep(uniform(2, 6))  # Evitamos sobrecargar el servidor
            
            if tries > 10:
                jobs_exceeded_time += 1
                print(f"Número de intentos excedido, SKIP! URL: {url}")
                continue  # Pasamos a la siguiente URL

            try:
                print(f"Num intentos: {tries}, URL: {url}")
                sopa = BeautifulSoup(res.content, "html.parser")

                # Sacamos la información de la oferta del script
                script_tag = sopa.find("script", {"type": "application/ld+json"})
                job_data = json.loads(script_tag.string)

                cleaned_job_data = {}

                cleaned_job_data["empleo"] = empleo
                cleaned_job_data["plataforma"] = "linkedin"

                cleaned_job_data["titulo_oferta"] = df.loc[i, "job_title"]
                cleaned_job_data["empresa"] = df.loc[i, "company_name"]
                cleaned_job_data["fecha_publicacion"] = df.loc[i, "job_listed"]
                
                # cleaned_job_data["company_location"] = df.loc[i, "company_location"]
                # cleaned_job_data["title"] = job_data.get("title")
                # cleaned_job_data["datePosted"] = job_data.get("datePosted")
                # cleaned_job_data["company"] = job_data.get("hiringOrganization").get("name")
                # cleaned_job_data["locality"] = job_data.get("jobLocation").get("address").get("addressLocality")
                cleaned_job_data["tipo_empleo"] = job_data.get("employmentType")
                cleaned_job_data["url_oferta"] = df.loc[i, "job_detail_url"]

                # Decodificamos la descripcion
                decoded_description = html.unescape(job_data.get("description"))
                cleaned_job_data["descripcion_original"] = decoded_description

                soup_description = BeautifulSoup(decoded_description, "html.parser")
                plain_text = soup_description.get_text()
                cleaned_job_data["descripcion"] = plain_text
                
                # Almacenamos en cada iteración los datos extraidos
                df_jobs = pd.concat([df_jobs, pd.DataFrame([cleaned_job_data])], ignore_index=True)
                df_jobs.to_csv(f"data/datos_descripcion_ofertas/linkedin_{empleo}.csv")
            
            except:
                print(f"Error en el link: {url}")

        print(f"No se pudo acceder a {jobs_exceeded_time} ofertas puesto que se excedieron los intentos.")

    return
    
