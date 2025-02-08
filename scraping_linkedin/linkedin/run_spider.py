import subprocess
import os
from time import sleep

# Configuración del scraping
START_POINT = 0
MAX_TOTAL_JOBS = 1000 #Para que se ejecute 4 veces el while
BLOCK_SIZE = 250

empleos = ["data_science", "data_analyst", "data_engineer"]
#empleos = ["data_analyst"]

for empleo in empleos: 
    
    # Borramos el archivo si existiese
    file_path = f"data/linkedin_madrid_{empleo}.csv"
    absolute_path = os.path.abspath(file_path)
   
    if os.path.exists(absolute_path):
        os.remove(absolute_path)
    

    # Poblamos el archivo con los jobs
    spiders_executed = 0
    while START_POINT < MAX_TOTAL_JOBS:
        print("\n +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ \n")
        
        spiders_executed +=1
        print(f"Ejecutando spider {spiders_executed}")
        print(f"Ejecutando bloque desde: {START_POINT}")

        # Ejecuta el comando Scrapy como un subproceso
        subprocess.run(
            [
                "scrapy",
                "crawl",
                "linkedin_jobs",
                "-a",
                f"START_POINT={START_POINT}",
                "-a",
                f"SEARCH_TERM={empleo}"
            ]
        )
        # Incrementa el punto de inicio
        START_POINT += BLOCK_SIZE
        sleep(3)

    print(f"Scraping completado con {spiders_executed} spiders.")
