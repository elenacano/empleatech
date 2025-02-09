# Módulos de Selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select 

# Otros módulos
import undetected_chromedriver as uc # type: ignore
import os
from dotenv import load_dotenv
import time
import random
from bs4 import BeautifulSoup # type: ignore
import requests as req
from webdriver_manager.chrome import ChromeDriverManager  # type: ignore
from selenium.webdriver.chrome.options import Options # type: ignore
from zenrows import ZenRowsClient # type: ignore
from datetime import datetime

# Pandas para manejo de datos
import pandas as pd
import numpy as np
import re

from time import sleep

load_dotenv()

def guardar_ofertas_df(driver, df, empleo):
    
    # Vamos bajando y entrando en cada oferta
    for i in range(1,28):
        print("-------------------------------------------------------")
        try:
            elemento_lista = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="app"]/div/div[3]/div[1]/div[3]/main/ul/li[{i}]')))
            elemento_lista.click()
            time.sleep(random.uniform(3,7))

            contenedor = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#main-wrapper > div > div.container.container-slotbanner > div:nth-child(3) > div.container-expanded.panel-default > div > div.col-8.col-12-medium > div > div.inner.inner-expanded.panel-canvas.panel-rounded')))
            contenedor_texto = contenedor.text

            cabecera = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#main-wrapper > div > div.container.container-slotbanner > div:nth-child(3) > div.panel-canvas.panel-rounded')))
            cabecera_texto = cabecera.text
            print(driver.current_url)
            print(cabecera_texto)

            datos_oferta = {
                        "empleo" : empleo,
                        "url_oferta" : driver.current_url,
                        "cabecera": cabecera_texto,
                        "contenido": contenedor_texto
            }

            df_aux = pd.DataFrame([datos_oferta])
            df = pd.concat([df, df_aux], ignore_index=True)

            df.to_csv(f"datos_crudo/infojobs_{empleo}.csv")

            print(f"Datos de la oferta {i} guardados correctamente.")

            #Volvemos a la pagina principal
            driver.back()
            sleep(random.uniform(3,7))
            driver.execute_script("window.scrollBy(0, 200);")
            sleep(random.uniform(0.3, 0.8))

        except:
            print(f"\nFallo en el elemento de la lista: {i}\n")
            driver.execute_script("window.scrollBy(0, 200);")
            sleep(random.uniform(0.3, 0.8))
            
    return df


def extraccion_ofertas_infojobs():
    URL = 'https://www.infojobs.net/'   
    usuario = os.getenv('user_infojobs') 
    clave = os.getenv('password_infojobs')

    # Creamos la carpeta donde se van a guardar los resultados si no existe
    file_path = "datos_crudo"
    absolute_path = os.path.abspath(file_path)

    if not os.path.exists(absolute_path):
        os.makedirs(absolute_path)


    # Inicializmos el driver
    driver = uc.Chrome(version_main=132, headless=False,use_subprocess=False)
    driver.get(URL)

    df = pd.DataFrame()
    diccionario_puestos = {
        "data_analyst" : "https://www.infojobs.net/jobsearch/search-results/list.xhtml?keyword=analista+de+datos&normalizedJobTitleIds=&provinceIds=33&countryIds=17&cityId=&searchByType=province",
        "data_science" : "https://www.infojobs.net/ofertas-trabajo?keyword=Data%20scientist&provinceIds=33&sortBy=RELEVANCE&countryIds=17&sinceDate=ANY",
        "data_engineer" : "https://www.infojobs.net/ofertas-trabajo?keyword=Data%20engineer&provinceIds=33&sortBy=RELEVANCE&countryIds=17&sinceDate=ANY"
    }

    sleep(4)

    # intenta encontrar las cookies y aceptar, si no encuentra imprime ya tiene las cookies
    try:
        driver.find_element(By.CSS_SELECTOR, '#didomi-popup > div > div')
        driver.execute_script("window.scrollTo(0, 1000);")
        driver.find_element(By.CSS_SELECTOR, '#didomi-notice-agree-button').click()
        
        print('Cookies aceptadas')
        
    except Exception as e:
        print(e)
        print('Ya tienes la cookies')


    #hacer click en acceso a candidatos
    driver.find_element(By.CSS_SELECTOR, '#candidate_login').click()
    cuadro_usuario= WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#email')))

    for letra in usuario:
        cuadro_usuario.send_keys(letra)
    cuadro_clave= driver.find_element(By.CSS_SELECTOR, '#id-password')
    for num in clave:
        cuadro_clave.send_keys(num)
    cuadro_usuario.submit()
    sleep(3)

    #Cargamos la página de los trabajos en Madrid
    for empleo, url_empleo in diccionario_puestos.items():
        print(f"\n ------------------------BUSCANDO OFERTAS PARA {empleo}---------------------------\n")

        driver.get(url_empleo)
        sleep(random.uniform(3,7))

        pag=1
        
        while True:

            print(f"\n *** \n Página {pag}, filas df: {df.shape[0]}")

            df = guardar_ofertas_df(driver, df, empleo)

            try:
                sleep(15)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(1)
                driver.execute_script("window.scrollBy(0, -200);")
                sleep(3)

                lista_elementos = driver.find_elements(By.CSS_SELECTOR, "ul.sui-MoleculePagination > li")

                if lista_elementos:
                    ultimo_elemento = lista_elementos[-1]
                    
                    texto_boton = ultimo_elemento.text.strip()
                    print(texto_boton)

                    if texto_boton.upper() == "SIGUIENTE":
                        pag +=1
                        boton = ultimo_elemento.find_element(By.TAG_NAME, "button")
                        boton.click()
                    else:
                        print("\nNo hay más páginas")
                        break
                else:
                    print("No se encontraron elementos en la lista.")

            except:
                print("\n\nNo hay más páginas")
                break

        driver.quit()


def procesar_cabecera(cabecera):
        partes = cabecera.split("\n")
        job_title, company_name = None, None
        min_salary, max_salary = np.nan, np.nan
        fecha_publicacion = np.nan

        if partes[1] in ["Proceso online", "Executive"]:
            job_title, company_name = partes[2], partes[3]
        else:
            job_title, company_name = partes[1], partes[2]

        for parte in partes:
            if "salario" in parte.lower():
                if parte.lower() == "salario no disponible":
                    min_salary, max_salary = np.nan, np.nan
                else:
                    palabras = parte.split()
                    min_salary, max_salary = palabras[1], palabras[3]

            if "publicada" in parte.lower():
                fecha_publicacion = parte

        return job_title, company_name, fecha_publicacion, min_salary, max_salary

def extraer_datos_cabecera_infojobs():

    file_path = "datos_limpios"
    absolute_path = os.path.abspath(file_path)

    if not os.path.exists(absolute_path):
        os.makedirs(absolute_path)


    empleos = ["data_science", "data_analyst", "data_engineer"]

    for empleo in empleos:
        df = pd.read_csv(f"datos_crudo/infojobs_{empleo}.csv", index_col=0)

        # Usar .apply una sola vez para descomponer los valores
        df["plataforma"] = "infojobs"
        df[["titulo_oferta", "empresa", "fecha_publicacion", "min_salario", "max_salario"]] = df["cabecera"].apply(procesar_cabecera).apply(pd.Series)
        df["descripcion"] = df["contenido"]

        col = df.pop('url_oferta')  # Extrae la columna
        df.insert(9, 'url_oferta', col)

        df.drop(columns=["cabecera", "contenido"], inplace=True)

        df.to_csv(f"datos_limpios/infojobs_{empleo}.csv")

    print("Datos guardados correctamente")


def replace_newlines_with_br(text):
    return text.replace("\n", "<br>")

def job_description_to_html(text):
    text = text.strip()
  
    # Convertir títulos de sección en <h2>
    sections = [
        "Requisitos mínimos", "Requisitos", "Descripción"
    ]
    for section in sections:
        text = re.sub(rf"{section}", f"<br><h3>{section}</h3>", text)

    # Convertir subtítulos en <h3>
    subtitles = ["Estudios mínimos", "Experiencia mínima"]
    for subtitle in subtitles:
        text = re.sub(rf"\b{subtitle}\b", f"<h4>{subtitle}</h4>", text)


    # Convertir ciertas palabras clave en negrita
    text = re.sub(r"(BASIC QUALIFICATIONS|PREFERRED QUALIFICATIONS|El ideal candidato)", r"<strong>\1</strong><br>", text)

    return text

def limpieza_descripcion():
    empleos = ["data_science", "data_analyst", "data_engineer"]

    for empleo in empleos:
        df = pd.read_csv(f"datos_limpios/infojobs_{empleo}.csv", index_col=0)
        df["descripcion_original"] = df["descripcion"].apply(lambda x: replace_newlines_with_br(x))
        df["descripcion_original"] = df["descripcion_original"].apply(lambda x: job_description_to_html(x))
        display(df.head())

        porcentaje = round(df[df["min_salario"].notna()].shape[0]*100/df.shape[0],2)
        print(f'El porcentaje de ofertas con salario para {empleo} es: {porcentaje}%\n')

        df.to_csv(f"datos_limpios/infojobs_{empleo}.csv")