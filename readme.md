![alt text](imagenes/logo_sin_fondo_2.png)



# Funcionamiento paso a paso del Pipeline ETL:

## **1. Extracción**

### **Scrapeo de LinkedIn**

Para llevar a cabo el crapeo de LinkedIn hay que hacerlo en dos fases. La primera fase se realiza con scrapy, tenemos que acceder a la carpeta `scraping_linkedin\linkedin` y ejecutar el archivo run_spider.py. Automáticamente se almacenaran dentro de `scraping_linkedin\linkedin\data` tres archivos csv los cuales contienen la información básica de las ofertas de trabajo devueltas por un endpoint de la API de LinkedIn. Sin embargo, estas ofertas no están completas y necesitamos la descripción. Por lo tanto, dentro de estos csv podemos encontrar el link a cada oferta de donde podemos sacar la descripción y más detalles. Este proceso se lleva a cabo ejecutando el notebook `scraping_linkedin\detailed_job_info.ipynb` por lo que el siguiente paso el hacer un *run all* de dicho notebook. Una vez ejecutado, dentro de la carpeta `scraping_linkedin\data\datos_descripcion_ofertas` encontraremos tres csv, uno por cada empleo, con datos detallados de cada oferta: empleo, plataforma, titulo_oferta, empresa, fecha_publicacion, tipo_empleo, url_oferta,descripcion_original, descripcion. En este punto habremos concluido satisfactoriamnet el scrapeo de las ofertas de LinkedIn.

### **Scrapeo de Infojobs**

La ejecucuión de este scrapeo es un poco más tediosa, pues tras intentarlo de númerosas formas los captchas siempre terminaban por detectar el programa como un bot y no permitían el acceso a las ofertas. Por lo tanto, como se ha visto que el número de ofertas para cada empleo en esta plataforma no suele ser más de 100 se ha implementado un scrapeo supervisado con Selenium. El programa accede a través de una cuenta de infojobs y comienza la búsqueda imitando el comportamiento humano para evitar ser detetado, sin embargo, puede saltar un captha por lo que hay que estar atento y resolverlo rápidamente. A pesar de ser un inconveniente no siempre saltan y ahorramos mucho más tiempo que si hicieramos la recogida de datos a mano. En un futuro se plantea obtener la información de las ofertas de Infojobs a través de una API de pago. 

Loúnico que hay que hacer es rellenar las variables de `scraping_infojobs\.env.txt` on un usuario y contraseña de infojobs, a poder ser uno nuevo y no el personal por si acaso acaba baneado por actividad sospechosa. Una vez completadas las variables de entornos ejecutamos el notebook `scraping_infojobs\selenium_infojobs.ipynb` y los datos de todas las ofertas se irá almacenando en `scraping_infojobs\datos_crudo`. Finalmente para llevar a cabo una primera limpieza ejecutamos el notebook `scraping_infojobs\limpieza_datos.ipynb`, se estraeran datos relevantes de las cabeceras de las ofertas y se hará una limpieza de las descripciones, los datos limpios son almacenados en `scraping_infojobs\datos_limpios`. Y así se da por concluido todo elproceso de extracción de las ofertas.


## **2. Transformación**

El proceso de transformación y limpeza se lleva a cabo en la carpeta `limpieza_y_carga`, dentro se encontrará un notebook el cual se encarga de todo el proceso. 

El primer paso consiste en recorrer todos los archivos obtenidos en el paso anterior y de cada descripción extraer los años de experiencia que piden, el nivel de inglés, las hard skills necesarias, las hard skill deseables y un porcentaje de ajuste. Este porcetaje representa cuanto se ajusta la descripción de la oferta en cuanto al puesto para el que se realizó la busqueda, por ejemplo, Data analyst. Este proceso se lleva a cabo mediante la API de OpenAI con el modelo gpt-4o-mini. Para poder ejecutar el notebook necesitar darte de alta en [https://platform.openai.com/docs/overview](https://platform.openai.com/docs/overview). Una vez hayas obtenido tu API key rellena el campo *apikey_openai* en `limpieza_y_carga\.env.txt` y ya podreás ejecutar la primera parte del notebook para la extracción de las descripciones.

Después se lleva a cabo la limpieza de los JSON generados, lo agrupan mismas skills con distintos nombres y se filtran aquellas irrelevantes, una vez las skills está filtradas se guardan los archivos en la carpeta `limpieza_y_carga\data\skills_filtradas`. En total entre todas las ofertas hay una 3000 skills, tenemos que reducir este número, por lo que nos vamos a quedar con las skills que tengan un mínimo de 5 apariciones para cada tipo de empleo. Una vez tenemos esta lista, filtramos de nuevo las ofertas y toda aquella skill que no esté dentro de la lista de skill relevantes se elimina. Las ofertas filtradas ya con las skills relevantes se almacenan en `limpieza_y_carga\data\skills_filtradas_relevantes`. Además también se genera una lista con todas las skills relevantes que se puede consultar en `limpieza_y_carga\data\lista_hard_skills.pkl`. Como último paso las skills de esta lista son divididas en distintas categorías, para que la visualización de estas en la aplicación sea más amigable, aunque este sea un paso posterior ya hay que dejarlo preparado. La lista de skills categorizadas se encuentra en `limpieza_y_carga\data\diccionario_skills_categorizadas.pkl`.


## **3. Carga a la BBDD**
Para este proyecto hemos escogido una base de datos NoSQL, almacenaremos los datos en colecciones en el servidor de MongoAtlas. Para ello es necesario registrarse en [https://www.mongodb.com/es/cloud/atlas/register](https://www.mongodb.com/es/cloud/atlas/register). Creamos un usuario con nombre *root* y una password, esta contraseña la debemos añadir al archivo `limpieza_y_carga\.env.txt`. Finlmente cargamos los datos a una base de datos llamada *db_empleatech_v2*, este proceso de carga se lleva a cabo al final del notebook `limpieza_y_carga\transformacion_y_carga.ipynb`.
