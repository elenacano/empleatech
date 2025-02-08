![alt text](imagenes/logo_sin_fondo_2.png)



# Funcionamiento paso a paso:

## **1. Extracción**

### **Scrapeo de LinkedIn**

Para llevar a cabo el crapeo de LinkedIn hay que hacerlo en dos fases. La primera fase se realiza con scrapy, tenemos que acceder a la carpeta `scraping_linkedin\linkedin` y ejecutar el archivo run_spider.py. Automáticamente se almacenaran dentro de `scraping_linkedin\linkedin\data` tres archivos csv los cuales contienen la información básica de las ofertas de trabajo devueltas por un endpoint de la API de LinkedIn. Sin embargo, estas ofertas no están completas y necesitamos la descripción. Por lo tanto, dentro de estos csv podemos encontrar el link a cada oferta de donde podemos sacar la descripción y más detalles. Este proceso se lleva a cabo ejecutando el notebook `scraping_linkedin\detailed_job_info.ipynb` por lo que el siguiente paso el hacer un *run all* de dicho notebook. Una vez ejecutado, dentro de la carpeta `scraping_linkedin\data\datos_descripcion_ofertas` encontraremos tres csv, uno por cada empleo, con datos detallados de cada oferta: empleo, plataforma, titulo_oferta, empresa, fecha_publicacion, tipo_empleo, url_oferta,descripcion_original, descripcion. En este punto habremos concluido satisfactoriamnet el scrapeo de las ofertas de LinkedIn.

### **Scrapeo de Infojobs**
La ejecucuión de este scrapeo es un poco más tediosa, pues tras intentarlo de númerosas formas los captchas siempre terminaban por detectar el rograma como un bot y no permitían el acceso a las ofertas. Por lo tanto, como se ha visto que el número de ofertas para cada empleo en esta plataforma no suele ser más de 100 se ha implementado un scrapeo supervisdo con Selenium. El programa accede a través de una cuenta de infoobs y comienza la búsqueda imitando el comportamiento humano para evitar ser detetado, sin embargo, pueden saltar un capthas por lo que hay que estar atento y resolverlo rápidamente. A pesar de ser un inconveniente no siempre saltan y ahorramos mucho más tiempo que si hicieramos la recogida de datos a mano. En un futuro se plantea obtener la información de las ofertas de Infojobs a través de una API de pago. 

