from openai import OpenAI # type: ignore
from dotenv import load_dotenv # type: ignore
from difflib import SequenceMatcher
from tqdm import tqdm # type: ignore
import pandas as pd # type: ignore
import pickle
import json
import os
from src import prompts

diccionario_conversion = {
    'unix': 'Linux',
    'bases de datos relacionales': 'SQL',
    'relacionales': 'SQL',
    'bases de datos no relacionales': 'NoSQL',
    'no relacionales': 'NoSQL',
    'mongodb': 'NoSQL',
    'data warehousing': 'Data Warehouse',
    'herramientas de integración continua': 'CI/CD',
    'postgre': 'SQL',
    'postgres': 'SQL',
    'metodologías ágiles': 'Agile',
    'natural language processing': 'NLP',
    'elt': 'ETL',
    "go":"Golang",
    "no sql":"NoSQL",
    "no-sql":"NoSQL",
    "github":"Git",
    "gitlab":"Git",
    "git":"Git",
    "scala":"Scala",
    'data analytics': 'Data Analysis',
    'data warehouses': 'Data Warehouse',
    'big query': 'BigQuery',
    'business intelligence': 'BI (Business Intelligence)',
    'bi': 'BI (Business Intelligence)',
    'problem-solving': 'Problem solving skills',
    'problem solving': 'Problem solving skills',
    'dbt': 'DBT (Data Build Tool)',
    'gcp': 'GCP (Google Cloud Platform)',
    'data visualization': 'Data Visualization tools',
    'visualización de datos': 'Data Visualization tools',
    'microsoft suite': 'Microsoft Office',
    'data scientist': 'Data Science',
    'scikit-learn':'Sklearn',
    'Generative AI':'IA Generativa',
    'Análisis':'Analytical skills',
    'mathematics':'',
    'matemáticas':'',
    'trabajo en equipo': '',
    'comunicación efectiva': '',
    'gestión de proyectos': '',
    'análisis financiero': '',
    'documentación técnica': '',
    'finanzas': '',
    'modelado de datos': '',
    'automatización de procesos': '',
    'capacidad analítica': '',
    'consultoría': '',
    'consulting': '',
    'growth mindset': '',
    'testing': '',
    'communication': '',
    'atención al detalle': '',
    'gestión financiera': '',
    'programación': '',
    'resolución de problemas': '',
    'contabilidad': '',
    'networking': '',
    'team spirit': '',
    'collaboration skills': '',
    'ingeniería': '',
    'gestión del tiempo': '',
    'pruebas unitarias': '',
    'comunicación': '',
    'gestión de riesgos': '',
    'atención al cliente': '',
    'alemán': '',
    'conocimiento de productos bancarios': '',
    'communication strategy': '',
    'facilitation': '',
    'coaching': '',
    'stakeholder engagement': '',
    'spanish': '',
    'italian': '',
    'portuguese': '',
    "optimización":'',
    "toma de decisiones":'',
    "conocimientos de sistemas de planificación":'',
    "metodología":'',
    "trade Marketing":'',
    "reporting diario":'',
    "análisis cuantitativo y cualitativo":'',
    "francés":"",
    'communication skills': '',
    'interpersonal skills': '',
    'informatica':'',
    'communication': '',
    'crm':'',
    'corporate': '',
    'russian': '',
    'mindset': '',
    'degree': '',
    'project management': '',
    'french': '',
    'empresas':'',
    'disaster':'',
    'purestorage':'',
    'presto':'',
}

lista_habilidades_basicas = ["Python", "Power BI", "AWS", "ETL", "Excel", "Tableau", "Plotly", "Machine Learning", "Gitlab", "Github", 'Docker', "Oracle", "Linux", 'Jenkins', 'Databricks', 'Kubernetes', 'Snowflake', 'CI/CD', 'GCP', 'CSS', 'HTML',  'Hadoop', 'Terraform', 'Sklearn', 'PySpark', 'Spark', 'Big Data', 'Kafka', 'Airflow', 'Angular', 'MongoDB', 'NoSQL', "No SQL", "SQL", 'Ansible',  'Pandas', 'C#', 'Maven', 'Jira', 'Estadística', '.NET', 'Web scraping', 'REST', 'SAP', 'SOAP', 'API', 'Javascript',  "Java", 'C++', 'Salesforce', 'XML', 'DB2', 'Spring', 'PHP', 'Hibernate', 'React', 'DBT', 'Prometheus', 'MLOps', 'TensorFlow', 'PyTorch', 'VBA',  'Looker', 'SAS', 'Confluence', 'J2EE', 'Bash', 'Cloudera', 'Cloud', 'Data Visualization', 'Data Governance', 'Hive', 'NLP', 'TypeScript', 'Cobol',  'JSON', 'Agile', 'Qlik', "Scrum", "Shell", "Node", 'Vue','OAuth', "Bases de datos", "KPI", 'Next', 'Azure', 'PowerPoint', 'Análisis de datos', 'Visualización de datos', "Redes neuronales", "DevOps", 'relacionales', 'no relacionales', 'Data Analysis', 'Problem solving', 'Problem-solving', 'A/B testing', 'Data Mining', 'Transformers', 'Big Query', 'BigQuery', 'Hugging Face', 'Selenium', 'Business Intelligence', 'communication', 'QuickSight', 'Microsoft Office', 'Microsoft Suite', 'Matlab', 'Scikit-learn', 'Data Science', 'Data Scientist', 'Corporate', 'mindset', 'degree', 'crm', 'empresas', 'disaster']


diccionario_categorias_skills = {
    "Data Science & Machine Learning": [
        "AI", "NLP", "Sklearn", "PySpark", "Deep Learning", 
        "TensorFlow", "Machine Learning", "MLOps", "Data Science", "PyTorch", 
        "Pandas"
    ],
    "Big Data & ETL": [
        "Big Data", "Spark", "Databricks", "Hadoop", "Kafka", "ETL", "Airflow"
    ],
    "Business Intelligence & Analytics": [
        "Data Analysis","Análisis de datos", "Google Analytics", "Looker", "Data Visualization tools", "BI (Business Intelligence)", 
        "Power BI", "Qlik", "Tableau", "DAX", "Análisis" 
    ],
    "Bases de Datos": [
        "Bases de datos", "Oracle", "NoSQL", "BigQuery", "Hive", "Cassandra", "Snowflake", 
        "DB2", "SQL", "Data Warehouse"
    ],
    "Cloud & DevOps": [
        "Docker", "DevOps", "Terraform", "Cloud", "Azure", "GCP (Google Cloud Platform)", 
        "AWS", "OpenStack", "Kubernetes", "Ansible", "Prometheus"
    ],
    "Data Governance & Management": [
        "Data Modeling", "Data Management", "Data Governance", "DBT (Data Build Tool)"
    ],
    "Programación & Scripting": [
        "C", "C#", "Java", "C++", "VBA", "Kotlin", "Scripting", "Shell", "Bash", "Python", "R", "Django", "Flask"
    ],
    "Infraestructura & CI/CD": [
        "Git", "Jenkins", "CI/CD", "Maven"
    ],
    "Metodologías & Habilidades": [
        "Agile", "Scrum", "TDD", "Analytical skills", "Problem solving skills"
    ],
    "Desarrollo Backend": [
        "Node", "PHP", "Spring", "Scala", "Cobol",  
        "Microservicios", ".NET", "Ruby", "Hibernate", "Golang", "Rust", 
    ],
    "Desarrollo Frontend": [
        "Angular", "React", "Javascript", "HTML", "CSS", "TypeScript"
    ],
    "Herramientas Empresariales": [
        "SAS", "Confluence", "Jira", "SAP", "Salesforce", "Power Apps", "Microsoft Office", "MS Office", 
        "PowerPoint", "Excel"
    ],
    "Otros": [
        "REST", "API", "XML", "JSON", "Estadística", "Linux", "A/B testing",
    ]
}


def conexion_openai(api_key):
    print(load_dotenv())
    apikey_openai = os.getenv(api_key) 
    client = OpenAI(api_key=apikey_openai)
    return client


def get_prompt(empleo):
    if empleo.lower() == "analyst":
        prompt = prompts.get_data_analyst_prompt()
    elif empleo.lower() == "science":
        prompt = prompts.get_data_science_prompt()
    elif empleo.lower() == "engineer":
        prompt = prompts.get_data_engineer_prompt()
    else:
        return ''
    return prompt


def trasformacion_openai(client, empleo, oferta):
    prompt = get_prompt(empleo)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": f"{oferta}"
            }
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "job_analysis_schema",
                "schema": {
                    "type": "object",
                    "properties": {
                        "nivel_ingles": {
                            "type": "string",
                            "enum": ["A1", "A2", "B1", "B2", "C1", "C2", "No especificado"]
                        },
                        "anios_experiencia": {
                            "type": "string"
                        },
                        "porcentaje": {
                            "type": "string",
                            "pattern": "^[0-9]+$"
                        },
                        "skills_necesarias": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "skills_valoradas": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    },
                    "additionalProperties": False
                }
            }
        }
    )

    return completion.choices[0].message.content

def get_lista_ofertas():
    lista_ofertas=[]

    # Files de infojobs
    folder_path_infojobs = "../scraping_infojobs/datos_limpios/"
    files_infojobs = os.listdir(folder_path_infojobs)
    [lista_ofertas.append(folder_path_infojobs + file) for file in files_infojobs]

    # Files de linkedin
    folder_path_linkedin = "../scraping_linkedin/data/datos_descripcion_ofertas/"
    files_linkedin = os.listdir(folder_path_linkedin)
    [lista_ofertas.append(folder_path_linkedin + file) for file in files_linkedin]

    return lista_ofertas


def crear_carpetas_responese_openai():

    # Comprobamos que existe la carpeta data y si no la creamos
    file_path = "data"
    absolute_path = os.path.abspath(file_path)
    
    if not os.path.exists(absolute_path):
        os.makedirs(absolute_path)

    # Comprobamos que existe la carpeta response_openai dentro de data y si no la creamos
    file_path = "data/response_openai"
    absolute_path = os.path.abspath(file_path)
    
    if not os.path.exists(absolute_path):
        os.makedirs(absolute_path)


def elimiar_ofertas_repetidas():

    lista_ofertas = get_lista_ofertas()

    file_path = "data/ofertas_sin_duplicados"
    absolute_path = os.path.abspath(file_path)
    
    if not os.path.exists(absolute_path):
        os.makedirs(absolute_path)

    for file_path in lista_ofertas:

        nombre_file = file_path.split("/")[-1]
        
        # Cargamos el fichero
        df = pd.read_csv(file_path, index_col=0)

        # Eliminar duplicados basados en 'titulo_oferta' y 'empresa', conservando la primera aparición
        df = df.drop_duplicates(subset=['titulo_oferta', 'empresa'], keep='first')

        # Guardar el DataFrame limpio
        df.to_csv(f"data/ofertas_sin_duplicados/{nombre_file}", index=False)
  



def extracion_datos_descripciones():

    crear_carpetas_responese_openai()
    elimiar_ofertas_repetidas()
    client = conexion_openai('apikey_openai')

    # Obtenemos la lista de los df
    lista_ofertas=[]
    folder_path_linkedin = "data/ofertas_sin_duplicados/"
    files_linkedin = os.listdir(folder_path_linkedin)
    [lista_ofertas.append(folder_path_linkedin + file) for file in files_linkedin]
 
    for file_path in lista_ofertas:
        
        # Para cada fichero sacamos el tipo de empleo
        parte_final_file = file_path.split("/")[-1]
        nombre_file = parte_final_file.split(".")[0]
        empleo = nombre_file.split("_")[2]

        # Cargamos el fichero
        df = pd.read_csv(file_path, index_col=0)

        print(f"Analizando el archivo -{parte_final_file}- de la categoria: Data {empleo}, con shape: {df.shape}")

        json_data = []

        #for row in range(df.shape[0]):
        for row in range(min(200, df.shape[0])):

            # Hacemos un json con los datos de cada fila
            row_data = df.iloc[row].to_dict()

            if df.iloc[row]["plataforma"] == "infojobs":
                if pd.isna(df.iloc[row]["min_salario"]):
                    row_data["min_salario"] = "No especificado"

                if pd.isna(df.iloc[row]["max_salario"]):
                    row_data["max_salario"] = "No especificado"

            # Sacamos la descripción y llamamos a openai
            descripcion = row_data["descripcion"] 
            response_content = trasformacion_openai(client, empleo, descripcion)
            response_json = json.loads(response_content)
            row_data["transformacion"] = response_json
            
            # Agregar la fila al listado de datos en JSON y guardarla
            json_data.append(row_data)
            with open(f"data/response_openai/transformed_{nombre_file}.json", "w", encoding="utf-8") as json_file:
                json.dump(json_data, json_file, ensure_ascii=False, indent=4)


def contador_skills(folder_path):
    """
    Cuenta y devuelve las habilidades únicas presentes en los archivos JSON de una carpeta.

    Args:
        folder_path (str): Ruta a la carpeta que contiene los archivos JSON con las ofertas y habilidades.

    Returns:
        list[str]: Lista de habilidades únicas encontradas en los archivos.

    Detalles:
        - Lee todos los archivos JSON en la carpeta especificada.
        - Extrae las habilidades de los campos `skills_necesarias` y `skills_valoradas` de cada oferta.
        - Combina y elimina duplicados de las habilidades extraídas utilizando `set`.
        - Imprime en consola la cantidad total de habilidades únicas encontradas.
    """

    files_openai = os.listdir(folder_path)
    lista_skills = []

    print(f"Contando skills de los archivos: {files_openai}")

    for file in files_openai:
        
        file_path = os.path.join(folder_path, file)
        with open(file_path, 'r') as archivo:
            json_datos = json.load(archivo)

        for oferta in json_datos:
            lista_skills += oferta["transformacion"]["skills_necesarias"]
            lista_skills += oferta["transformacion"]["skills_valoradas"]
    
    lista_final= list(set(lista_skills))
    print(f"Se han encontrado {len(lista_final)} skills diferentes.\n")

    return lista_final

def filtro_skills(skill_original):
    """
    Filtra y estandariza una habilidad basándose en listas de referencia y reglas de similitud.

    Args:
        skill_original (str): La habilidad original que se desea filtrar o estandarizar.

    Returns:
        str: La habilidad transformada, estandarizada o la habilidad original si no se encuentra un mapeo válido.
    
    Detalles:
        - Convierte la habilidad a minúsculas para una comparación uniforme.
        - Verifica si la habilidad coincide con una clave en `diccionario_conversion`.
        - Compara la habilidad con una lista de habilidades básicas (`lista_habilidades_basicas`),
          utilizando coincidencia de subcadenas o similitud de más del 80% con `SequenceMatcher`.
    """

    skill = skill_original.lower()
    
    if skill in diccionario_conversion.keys():
        return diccionario_conversion[skill]

    for habilidad_basica_original in lista_habilidades_basicas:
        habilidad_basica = habilidad_basica_original.lower()

        if habilidad_basica in skill or SequenceMatcher(None, habilidad_basica, skill).ratio()>0.8:
            if habilidad_basica in diccionario_conversion.keys():
                return diccionario_conversion[habilidad_basica]
            else:
                return habilidad_basica_original

    return skill_original


def procesamiento_skills(skills, diccionario):
    """
    Procesa una lista de habilidades, estandarizándolas y actualizando un diccionario de transformaciones.

    Args:
        skills (list[str]): Lista de habilidades originales a procesar.
        diccionario (dict): Diccionario que almacena las transformaciones de habilidades originales a estandarizadas.

    Returns:
        tuple:
            - list[str]: Lista de habilidades transformadas y únicas.
            - dict: Diccionario actualizado con las transformaciones de habilidades.

    Detalles:
        - Utiliza `filtro_skills` para estandarizar cada habilidad en la lista.
        - Agrega las transformaciones al diccionario si la habilidad original es distinta de la transformada.
        - Evita duplicados en la lista de habilidades transformadas.
    """

    nuevas_skills = []

    for skill in skills:
        res = filtro_skills(skill)
        if skill != res:
            diccionario[skill] = res
        if res != '' and res not in nuevas_skills:
            nuevas_skills.append(res)
    
    return nuevas_skills, diccionario


def extraer_y_guardar_skills_filtradas():
    """
    Procesa y filtra las habilidades de archivos JSON en una carpeta, guardando los resultados en archivos nuevos.

    Args:
        None

    Returns:
        None

    Detalles:
        - Lee los archivos JSON desde la carpeta `data/response_openai/`.
        - Filtra las habilidades necesarias y valoradas de cada oferta utilizando `procesamiento_skills`.
        - Guarda los resultados procesados en la carpeta `data/skills_filtradas/` con el prefijo `filtered_`.
        - Muestra en consola el progreso de procesamiento para cada archivo.
    """

    folder_path_openai = "data/response_openai/"
    files_openai = os.listdir(folder_path_openai)
    diccionario_transformaciones = {}

    for file in files_openai:
        print(f"Filtrando las skills del archivo: {file}")
        lista_ofertas_nuevas_skills = []

        file_path = os.path.join(folder_path_openai, file)
        with open(file_path, 'r') as archivo:
            json_datos = json.load(archivo)

        for oferta in json_datos:
            transformacion = oferta["transformacion"]
            transformacion["skills_necesarias"], diccionario_transformaciones = procesamiento_skills(transformacion["skills_necesarias"], diccionario_transformaciones)
            transformacion["skills_valoradas"], diccionario_transformaciones = procesamiento_skills(transformacion["skills_valoradas"], diccionario_transformaciones)

            lista_ofertas_nuevas_skills.append(oferta)
            
            with open(f"data/skills_filtradas/filtered_{file}", "w", encoding="utf-8") as json_file:
                        json.dump(lista_ofertas_nuevas_skills, json_file, ensure_ascii=False, indent=4)
    
    print("\nSkills filtradas y guardadas correctamente.")

    #return diccionario_transformaciones #Para el debug
    return



def filtrar_skills_min_apariciones(respeticiones_min_skills=10):
    """
    Filtra habilidades relevantes según su frecuencia de aparición en archivos JSON y las guarda en un archivo pickle.

    Args:
        repeticiones_min_skills (int): Frecuencia mínima para considerar una habilidad como relevante (por defecto 10).

    Returns:
        list: Lista de habilidades relevantes filtradas.

    Guarda:
        - Un archivo `data/lista_hard_skills.pkl` con las habilidades relevantes.
    """

    skills_relevantes = set()

    folder_path = "data/skills_filtradas/"
    df_files = os.listdir(folder_path)
    skills_empleos={'analyst': {}, 'engineer': {}, 'science': {}}

    for file in df_files:

        df_data_transform = pd.read_json(folder_path + file)
        empleo = file.split(".")[0].split("_")[4]
        df_expanded = pd.json_normalize(df_data_transform['transformacion'])
        df_final = pd.concat([df_data_transform.drop(columns=['transformacion']), df_expanded], axis=1)

        for i in range(df_final.shape[0]):
            skills_necesarias = df_final["skills_necesarias"].iloc[i]
            skills_valoradas = df_final["skills_valoradas"].iloc[i]

            for skill in skills_necesarias+skills_valoradas:
                skills_empleos[empleo][skill] = skills_empleos[empleo].get(skill, 0) + 1

    # Una vez tenemos un diccionario con las skills de cada empleo, filtramos las skills más repetidas
    for empleo, skills in skills_empleos.items():
        for skill, valor in skills.items():
            if valor >= respeticiones_min_skills:
                skills_relevantes.add(skill)
    
    lista_hard_skills=list(skills_relevantes)

    with open('data/lista_hard_skills.pkl', 'wb') as archivo:
        pickle.dump(lista_hard_skills, archivo)
    print(f"Se han guardado {len(lista_hard_skills)} skills relevantes en 'data/lista_hard_skills.pkl'")

    # Una vez tenemos las skills las categorizamos
    skills_categorizadas = categorizar_skills(lista_hard_skills, diccionario_categorias_skills)
    with open('data/diccionario_skills_categorizadas.pkl', 'wb') as archivo:
        pickle.dump(skills_categorizadas, archivo)
    print(f"Se han categorizado las skills y almacenado en 'data/diccionario_skills_categorizadas.pkl'")


    return lista_hard_skills


# def extraer_hard_skills(lista_hard_skills):
#     client = conexion_openai('apikey_hard_skills')
#     completion = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[
#             {
#                 "role": "system",
#                 "content": ("Extrae y filtra habilidades técnicas específicas (hard skills) de una lista de habilidades. Los hard skills pueden incluir lenguajes de programación, herramientas específicas, y metodologías técnicas. Excluye cualquier soft skill, términos genéricos o habilidades personales. Devuelve el resultado como una lista de Python ordenada alfabéticamente, manteniendo el formato original de cada habilidad incluida."
#                                 "# Steps"
#                                 "\n1. **Identificación de hard skills**: Analiza cada elemento de la lista para determinar si es un hard skill o habilidad técnica."
#                                 "\n  - Incluye habilidades medibles como lenguajes de programación (e.g., Python, Java, Javascript), herramientas (e.g., Excel, AutoCAD, Azure, AWS, SAS, Saleforce), librerias, frameworks o microframeworks(e.g., Vue, Flask, Django) y metodologías (e.g., Scrum, Six Sigma)."
#                                 "\n  - Excluye habilidades interpersonales o cualquier habilidad personal."
#                                 "\n2. **Filtrado**: Crea una nueva lista con solo los hard skills identificados."
#                                 "\n3. **Ordenación**: Ordena la lista filtrada alfabéticamente."
#                                 "\n4. **Formato de salida**: Asegúrate de que todos los elementos mantengan el formato original proporcionado en la lista."

#                                "\n\n # Output Format"
#                                 "\n- Devuelve el resultado como una lista de Python ordenada alfabéticamente."

#                                 "\n\n# Examples"
#                                 "\n**Entrada**:\n"
#                                 "```python"
#                                ' ["Pandas", "pandas", "numpy", "Tensorflow","ReactJS","TypeScript","Github","SAS","Vue.js","Azure services","Neo4j","SparkSQL","Spark","PyTorch","C/C++", "Redes neuronales", "CI/CD practices", "Azure Dev-ops", "Azure Datafactory", "Red Hat", "Cloud Services", "PowerBi", "Azure SQL Data Warehouse", "Natural Language Processing", "Salesforce", "Microsoft Office Suite", "AutoCAD", "Cloud Infrastructure (AWS, Azure, GCP)", "Postgresql", "API Rest", "Nivel avanzado de Excel", "Numpy", "SciKit-Learn", "Next.js", "TensorFlow", "SnowFlake", "Pytorch", "PosgreSQL", "Deep Learning", "Contabilidad financiera", "Aleman", "PySpark", "Azure DataFactory", "Datawarehouse", "herramientas de análisis de datos", "Data Factory", "Visualización de datos", "Object Oriented Design", "Kubernettes", "Spring", "Proactive mindset", "Databricks", "Unit Testing", "Salesforce platform", "AUTOCAD", "Análisis de negocio", "Microsoft Suite", "Cobol", "FastAPI", "RestAPI", "Integración APIs", "Microstrategy", "Data Warehouse Design", "Series temporales", "Comunicación efectiva", "Data Visualization (Looker, Tableau, Power BI)", "Oracle PLSQL", "Generación de gráficos complejos", "Oracle", "SAS Guide", "JIRA", "Herramientas de Google Cloud", "Experiencia en Proyectos de Gobernanza del dato", "Scipy", "Dockers", "Qlikview", "Angular", "PowerBI avanzado", "Puppet", "Ingeniería Aeronáutica", "Data Lake Architecture", "non-relational databases", "Gestión de proyectos de desarrollo informático", "Problem-solving", "git", "CI/CD", "RESTful API", "Power Query", "Data Lake Architecture", "Programación C#", "middleware", "Microsoft Word", "CSS", "JQuery",  "Pipelines CI/CD",  "PHP"] '
#                                 "```"

#                                 "\n**Salida esperada**\n:"
#                                 "```python"
#                                 '["Pandas", "pandas", "numpy", "Tensorflow","ReactJS","TypeScript","Github","SAS","Vue.js","Azure services","Neo4j","SparkSQL","Spark","PyTorch","C/C++", "Redes neuronales", "CI/CD practices", "Azure Dev-ops", "Azure Datafactory", "Red Hat", "Cloud Services", "PowerBi", "Azure SQL Data Warehouse", "Natural Language Processing", "Salesforce", "Microsoft Office Suite", "AutoCAD", "Cloud Infrastructure (AWS, Azure, GCP)", "Postgresql", "API Rest", "Nivel avanzado de Excel", "Numpy", "SciKit-Learn", "Next.js", "TensorFlow", "SnowFlake", "Pytorch", "PosgreSQL", "Deep Learning", "PySpark", "Azure DataFactory", "Datawarehouse", "Visualización de datos", "Kubernettes", "Spring", "Databricks", "Salesforce platform", "AUTOCAD", "Microsoft Suite", "Cobol", "FastAPI", "RestAPI", "Integración APIs", "Data Warehouse Design", "Series temporales", "Data Visualization (Looker, Tableau, Power BI)", "Oracle PLSQL", "Oracle", "SAS Guide", "JIRA", "Herramientas de Google Cloud", "Scipy", "Dockers", "Qlikview", "Angular", "PowerBI avanzado", "Puppet", "Data Lake Architecture", "non-relational databases", "git", "CI/CD", "RESTful API", "Power Query", "Data Lake Architecture", "Programación C#", "Microsoft Word", "CSS", "JQuery",  "Pipelines CI/CD",  "PHP"]'
#                                 "```"

#                                 "\n\n# Notes"

#                                 #"\n- Puedes asumir que los elementos que necesitan ser filtrados estarán presentes en un contexto técnico claro."
#                                 #"\n- Si un término es ambiguo pero generalmente no considerado un hard skill, exclúyelo."
#                                 "\n- Las listas de ejemplos pueden ser más largas y complejas en aplicaciones reales."
#                                 "\n- Ten en cuenta que estas skills son referentes a puestos tecnológicos como data science, por lo que se deben incluir tecnologías relacionadas con ese sector como manejo de APIs, uso de tecnologías cloud, SAS, Salesforce, uso de librerías como numpy, pandas, SciKit-Learn, vue.js, angular, tensorflow, etc."
#                 )
#             },
#             {
#                 "role": "user",
#                 "content": f"{lista_hard_skills}"
#             }
#         ]
#     )
#     return completion.choices[0].message.content


# def limpieza_skills(lista_hard_skills, skills_json, diccionario_conversion):

#     lista_final_skills_json = []
   
#     for skill_json in skills_json:

#         # Para cada skill comprobamos si está en la lista de hard skills
#         if skill_json in lista_hard_skills:
#             lista_final_skills_json.append(skill_json)

        
#         else:
#             # Iteramos sobre la lista de hard skills
#             for hard_skill in lista_hard_skills:

#                 hard_skill_lower = hard_skill.lower()
#                 skill_json_lower = skill_json.lower()

#                 # Comprobamos si la skill está en el diccionario de conversiones
#                 if  diccionario_conversion.get(skill_json):
#                     lista_final_skills_json.append(diccionario_conversion[skill_json])
#                     break

#                 # Comprobamos si las palabras en minuscula son iguales o si alguna de las palabras de la skill está en la lista de hard skills
#                 elif (skill_json_lower == hard_skill_lower) or (hard_skill_lower in skill_json_lower.split()) or (skill_json_lower in hard_skill_lower.split()):
#                     lista_final_skills_json.append(hard_skill)
#                     diccionario_conversion[skill_json] = hard_skill
#                     break
                    
#                 # Comprobamos si la similitud entre las palabras es mayor al 70%
#                 elif SequenceMatcher(None, hard_skill_lower, skill_json_lower).ratio() > 0.75:
#                     lista_final_skills_json.append(hard_skill)
#                     diccionario_conversion[skill_json] = hard_skill
#                     break
                    

#     return lista_final_skills_json, diccionario_conversion


# def filtracion_hard_skills():

#     diccionario_conversion_general = {}

#     # Cargamos la lista de hard skills
#     with open('data/lista_hard_skills.pkl', 'rb') as archivo:
#         lista_hard_skills = pickle.load(archivo)

#     # Vamos recorriendo todos los archivos de las skills filtradas 
#     folder_path_openai = "data/response_openai/"
#     files_openai = os.listdir(folder_path_openai)

#     for file in files_openai:

#         nombre_file = folder_path_openai + file
#         with open(f'{nombre_file}', 'r') as archivo:
#             json_datos = json.load(archivo)

#         lista_ofertas_nuevas_skills = []

#         # Para cada oferta revisamos sus skills necesarias y valoradas y comprobamos si coinciden con alguna de la lista final de las hard skills
#         for oferta in tqdm(json_datos):

#             skills_necesarias = oferta["transformacion"]["skills_necesarias"]
#             skills_valoradas = oferta["transformacion"]["skills_valoradas"]

#             # Limpiamos las skills necesarias
#             lista_final_skills_necesarias, diccionario_conversion = limpieza_skills(lista_hard_skills, skills_necesarias, diccionario_conversion_general)
#             diccionario_conversion_general.update(diccionario_conversion)
#             oferta["transformacion"]["skills_necesarias"] = lista_final_skills_necesarias

#             # Limpiamos las skills valoradas
#             lista_final_skills_valoradas, diccionario_conversion = limpieza_skills(lista_hard_skills, skills_valoradas, diccionario_conversion_general)
#             diccionario_conversion_general.update(diccionario_conversion)
#             oferta["transformacion"]["skills_valoradas"] = lista_final_skills_valoradas

#             lista_ofertas_nuevas_skills.append(oferta)

#             # Guardamos las ofertas en un nuevo archivo con las skills filtradas
#             with open(f"data/skills_filtradas/filtered_{file}", "w", encoding="utf-8") as json_file:
#                 json.dump(lista_ofertas_nuevas_skills, json_file, ensure_ascii=False, indent=4)

    
#     return diccionario_conversion_general

def limpieza_skills_oferta(skills_json, lista_hard_skills):

    lista_final_skills_json = []
   
    for skill_json in skills_json:

        # Para cada skill comprobamos si está en la lista de hard skills más relevantes
        if skill_json in lista_hard_skills:
            lista_final_skills_json.append(skill_json)

    return lista_final_skills_json



def control_errores_ingles_porcentaje_experiencia(oferta):

    niveles_validos = {"A1", "A2", "B1", "B2", "C1", "C2", "No especificado"}


    nivel_ingles = oferta["transformacion"]["nivel_ingles"]
    anios_experiencia = oferta["transformacion"]["anios_experiencia"]
    porcentaje = oferta["transformacion"]["porcentaje"]

    # Comprobación del nivel de inglés
    if nivel_ingles not in niveles_validos:
        if nivel_ingles[:2] in niveles_validos:
            oferta["transformacion"]["nivel_ingles"] = nivel_ingles[:2]
        
        else:    
            print("\nError en el campo de ingles:")
            print(oferta["transformacion"])
        
    # Comprobación del porcentaje
    try:
        num_porc = int(porcentaje)
        if num_porc>100 or num_porc<0:
            print("\nErro en el campo de porcentaje:")
            print(oferta["transformacion"])
    except:
        print("\nPorcentaje no convertible a int:")
        print(oferta["transformacion"])
        
    # Comprobación de años de experiencia
    try:
        if anios_experiencia != "No especificado":

            if anios_experiencia.lower() == "no requerida":
                oferta["transformacion"]["anios_experiencia"]="No especificado"

            elif anios_experiencia[0] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]:
                oferta["transformacion"]["anios_experiencia"]=anios_experiencia[0]

            else:
                num_anios_experiencia = int(anios_experiencia)
                if num_anios_experiencia>15 or num_anios_experiencia<0:
                    print("\Error en el campo de experiencia:")
                    print(oferta["transformacion"])

    except:
        print("\nAños de experiencia no convertible a int:")
        print(oferta["transformacion"])
        print(anios_experiencia[0])

    if oferta["plataforma"]=="infojobs":
        if pd.isna(oferta["min_salario"]):
            oferta["min_salario"] = "No especificado"
        
        if pd.isna(oferta["min_salario"]):
            oferta["max_salario"] = "No especificado"


    return oferta



def filtracion_hard_skills_relevantes():

    # Vamos recorriendo todos los archivos de las skills filtradas 
    folder_path_openai = "data/skills_filtradas/"
    files_openai = os.listdir(folder_path_openai)

    # Cargamos la lista de hard skills
    with open('data/lista_hard_skills.pkl', 'rb') as archivo:
        lista_hard_skills = pickle.load(archivo)

    print("\nLimpiando las skills de las ofertas, manteniendo solo las más relevantes...\n")

    for file in files_openai:

        nombre_file = folder_path_openai + file
        with open(f'{nombre_file}', 'r') as archivo:
            json_datos = json.load(archivo)

        lista_ofertas_nuevas_skills = []

        # Para cada oferta revisamos sus skills necesarias y valoradas y comprobamos si coinciden con alguna de la lista final de las hard skills
        for oferta in tqdm(json_datos):

            oferta_filtrada = control_errores_ingles_porcentaje_experiencia(oferta)

            skills_necesarias = oferta_filtrada["transformacion"]["skills_necesarias"]
            skills_valoradas = oferta_filtrada["transformacion"]["skills_valoradas"]

            # Limpiamos las skills necesarias y valoradas para quedranos solo con las más relevantes
            oferta_filtrada["transformacion"]["skills_necesarias"] = limpieza_skills_oferta(skills_necesarias, lista_hard_skills)
            oferta_filtrada["transformacion"]["skills_valoradas"] = limpieza_skills_oferta(skills_valoradas, lista_hard_skills)

            lista_ofertas_nuevas_skills.append(oferta_filtrada)

            # Guardamos las ofertas en un nuevo archivo con las skills filtradas
            with open(f"data/skills_filtradas_relevantes/relevant_{file}", "w", encoding="utf-8") as json_file:
                json.dump(lista_ofertas_nuevas_skills, json_file, ensure_ascii=False, indent=4)

    print("\nCompletado!")

    return 

def eliminar_duplicados_ofertas_final():
    folder_path_openai = "data/skills_filtradas_relevantes/"
    files_openai = os.listdir(folder_path_openai)


    for file in files_openai:

        dic_sin_duplicados = {}
        ofertas_file = []
        repetidas = 0

        nombre_file = os.path.join(folder_path_openai, file)
        
        with open(nombre_file, 'r', encoding='utf-8') as archivo:
            json_datos = json.load(archivo)

        print(f"El archivo tiene {len(json_datos)} ofertas")

        for oferta in tqdm(json_datos, desc=f"Procesando {file}"):

            titulo = oferta.get("titulo_oferta", "").strip().lower()
            empresa = oferta.get("empresa", "").strip().lower()
            descripcion = oferta.get("descripcion", "").strip().lower()
            clave_oferta = (titulo, empresa, descripcion)  # Clave única de la oferta
            
            if titulo==None or titulo=="" or empresa==None or descripcion==None:
                continue

            if clave_oferta in dic_sin_duplicados.keys():
                repetidas += 1
                len_skills_nueva = len(oferta["transformacion"]["skills_necesarias"]) + len(oferta["transformacion"]["skills_valoradas"])
                len_skills_lista = len(dic_sin_duplicados[clave_oferta]["transformacion"]["skills_necesarias"]) + len(dic_sin_duplicados[clave_oferta]["transformacion"]["skills_valoradas"])
                
                # print(f'{oferta["transformacion"]["skills_necesarias"]}\n{oferta["transformacion"]["skills_valoradas"]}')
                # print(len_skills_nueva)
                # print("\n")
                # print(f'{dic_sin_duplicados[clave_oferta]["transformacion"]["skills_necesarias"]}\n{dic_sin_duplicados[clave_oferta]["transformacion"]["skills_valoradas"]}')
                # print(len_skills_lista)
                # print("---------------------------------------------------")

                if len_skills_nueva>len_skills_lista:
                    ofertas_file.remove(dic_sin_duplicados[clave_oferta])
                    ofertas_file.append(oferta)

            else:
                dic_sin_duplicados[clave_oferta] = oferta
                ofertas_file.append(oferta)

        with open(f"data/skills_filtradas_relevantes/{file}", "w", encoding="utf-8") as json_file:
            json.dump(ofertas_file, json_file, ensure_ascii=False, indent=4)


        print(f"El archivo tiene {repetidas} ofertas repetidas")
        print(f"La lista final de ofertas es de {len(ofertas_file)}")
        print("---------------")

def categorizar_skills(lista_hard_skills, diccionario_categorias_skills):
    base_categorias_skills = {categoria: [] for categoria in diccionario_categorias_skills}

    # Crear un diccionario inverso para búsqueda rápida
    skill_to_categoria = {
        skill: categoria
        for categoria, skills in diccionario_categorias_skills.items()
        for skill in skills
    }

    # Asignar cada skill de la lista a su categoría correspondiente
    for skill in lista_hard_skills:
        categoria = skill_to_categoria.get(skill, "Otros")
        if categoria:
            base_categorias_skills[categoria].append(skill)

    return base_categorias_skills