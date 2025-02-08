def get_data_science_prompt():
    prompt = ("Analiza ofertas de trabajo para el puesto de 'Data Science' y responde con un JSON estructurado según los criterios especificados."
            "- Extrae elementos clave de la oferta relacionados con el nivel de inglés, experiencia, adecuación al rol de Data Science, y habilidades necesarias y valoradas.\n\n"
            "# Output Format\n"
            "Proporciona la respuesta en el siguiente formato JSON:\n"
            "```json\n"
            "{\n"
            '    "nivel_ingles": "[Marco europeo (A1, A2, B1, B2, C1, C2) o \'No especificado\'],"\n'
            '    "anios_experiencia": "[Número de años de experiencia requeridos o \'No especificado\'],"\n'
            '    "porcentaje": "[Porcentaje del 0 al 100],"\n'
            '    "skills_necesarias": ["[Lista de hard skills necesarias]"],\n'
            '    "skills_valoradas": ["[Lista de hard skills valoradas]"]\n'
            "}\n"
            "```\n\n"
            "# Steps\n"
            "1. **nivel_ingles:** Busca las menciones relacionadas con el inglés en la oferta. Traduce estas menciones al marco europeo adecuado. "
            "Indica 'No especificado' si no se menciona.\n"
            "2. **anios_experiencia:** Localiza cualquier mención al número de años de experiencia requerida. Deja 'No especificado' si no hay datos claros.\n"
            "3. **porcentaje:** Analiza la oferta de trabajo y compararla con el perfil típico de un data science. Proporciona una evaluación objetiva que incluya una puntuación del 1 al 100, basada en cuánto encaja la oferta con las responsabilidades, habilidades y tecnologías características de un data science.\n"
            "4. **skills_necesarias:** Identifica y lista las hard skills exigidas. Excluye habilidades blandas.\n"
            "5. **skills_valoradas:** Haz una lista de las hard skills deseables pero no necesarias.\n\n"
            "# Notes\n"
            "- **Hard Skills:** Considera lenguajes de programación, herramientas, frameworks, bases de datos, técnicas de análisis o cualquier especificación tecnológica o metodológica.\n"
            "- **Nivel de inglés:** Asegura que cada descripción del nivel de inglés se traduzca correctamente al equivalente en el marco europeo.\n"
            "- Proporciona una evaluación objetiva basada únicamente en la información proporcionada en la oferta.\n\n"
            "# Examples\n\n"
            "**Example 1:**\n"
            "'Estamos buscando un Data Science con Experiencia mínima\nMás de 5 años\nIdiomas requeridos\nInglés - Nivel Intermedio\nRequisitos mínimos:-Más de 5 años de experiencia con Python-Más de 3 años de experiencia con IA-Experiencia con SQL\n-Experiencia con Machine Learning-Nivel avanzado de inglés. Será un plus:-Experiencia con AWS-Experiencia con PySpark-Experiencia con Snowflake-Experiencia con Salesforce"
            "**JSON resultante:**\n"
            "```json\n"
            "{\n"
            '    "nivel_ingles": "B2",\n'
            '    "anios_experiencia": "5",\n'
            '    "porcentaje": "95",\n'
            '    "skills_necesarias": ["Python", "SQL", "Machine Learning"],\n'
            '    "skills_valoradas": ["AWS","PySpark","Snowflake","Salesforce"]\n'
            "}\n"
            "```\n"
            "**Example 2:**\n"
            "'Eestamos seleccionando un INGENIERO/A DE DATOS con al menos 2 años.\nIdiomas requeridos\nInglés - Nivel Avanzado\nConocimientos necesarios\nPython\nBases de datos\nC++\nClearCase\nGit\nETL\nLinux\nAnálisis de datos\nBig data\nModelado de datos\nRequisitos mínimos\n-Cloud u Open Source.\n-PowerBI\n-Python: Avanzado\n-C++: Medio\n-ClearCase: Medio\n-Git: Medio\n-Linux: Medio\nDescripción\nRESPONSABILIDADES EN PROYECTO:\n-Participación en el proceso de diseño y creación de pipelines con herramientas Cloud u Open Source.\n-Programación en Python: conocimiento de programación Orientada a Objetos, diseño y creación de transformaciones de datos, optimización flujos, análisis de datos.\n-Modelado de Datos: physical data modelling y logical data modelling Migración de tecnología de ETL a stack Cloud u Open Source Hard Skills\n-Imprescindible tener experiencia en: Linux y bash scripting.\n-Destreza con bases de datos relacionales y no relacionales.\n-Analítica de datos usando Python Analítica de datos usando herramientas de Business Intelligence como Power BI.\nDESEABLE:\n-Control y conocimiento para el almacenamiento eficiente de grandes volúmenes de datos.\n-Experiencia en optimización de sistemas de procesamiento.\n-Experiencia con herramientas de procesamiento como Spark o Kafka.\n-Manejo con herramientas de orquestación como Airflow o similares.\n- Conocimiento de arquitecturas cloud como Azure o AWS."
            "**JSON resultante:**\n"
            "```json\n"
            "{\n"
            '    "nivel_ingles": "C1",\n'
            '    "anios_experiencia": "2",\n'
            '    "porcentaje": "65",\n'
            '    "skills_necesarias": ["Cloud", "PowerBI", "Python", "C++", "ClearCase", "Git", "Linux", "ETL"],\n'
            '    "skills_valoradas": ["Spark","Kafka","Airflow","Azure","AWS"]\n'
            "}\n"
            "```\n"
            "**Example 3:**\n"
            "Buscamos un Data Analyst con al menos 2 años de experiencia en Madrid para analizar datos complejos, generar insights accionables y colaborar con equipos multidisciplinarios para apoyar la toma de decisiones estratégicas.\nFunciones:\n- Diseñar, desarrollar y ejecutar análisis de datos utilizando Python y SQL para responder preguntas clave del negocio.\n- Crear visualizaciones dinámicas y reportes interactivos en Power BI para comunicar insights de manera clara y efectiva.\n- Colaborar con equipos de negocio para identificar necesidades analíticas y traducirlas en soluciones basadas en datos.\n- Optimizar procesos de recolección, limpieza y transformación de datos para garantizar su calidad e integridad.\n- Uso de tecnologías: Python, SQL, analítica de datos, machine Learning, Power BI, Azure, AWS y Spark.\nNecesitamos:\n- Al menos 2 años de experiencia en un puesto similar.\n- Nivel de inglés: mínimo B2\n"
            "**JSON resultante:**\n"
            "```json\n"
            "{\n"
            '    "nivel_ingles": "B2",\n'
            '    "anios_experiencia": "2",\n'
            '    "porcentaje": "70",\n'
            '    "skills_necesarias": ["Python", "SQL", "Power BI", "Azure", "Machine Learning", "AWS", "Spark"],\n'
            '    "skills_valoradas": []\n'
            "}\n"
            "```\n"
            "**Example 4:**\n"
            "Estamos en búsqueda de un/a Ingeniero/a de datos que con experiencia mínima\nAl menos 3 años\nRequisitos mínimos\n-Experiencia de al menos 3 años como desarrollador de BI o científico de datos.\n- Experiencia de al menos 3 años en diseño de almacenes de datos y minería de datos.\n- Conocimiento nivel avanzado en consultas SQL y lenguajes de programación de analítica de datos: Python.\n- Conocimiento de bases de datos no relacionales (MongoDB).\n- Valorable conocimientos en Spark o Databricks.\nRequisitos deseados\nSe valorará la posesión de certificado de discapacidad. Las funciones que llevará a cabo son:\n- Diseñar, construir e implementar soluciones de BI (a través de herramientas de informes y de procesos ETL/ELT).\n- Desarrollar y ejecutar consultas de bases de datos y realizar análisis."
            "```json\n"
            "{\n"
            '    "nivel_ingles": "No especificado",\n'
            '    "anios_experiencia": "3",\n'
            '    "porcentaje": "80",\n'
            '    "skills_necesarias": ["BI", "Diseño de almacenes de datos", "Minería de datos", "SQL" , "Python", "MongoDB", "ETL/ELT"],\n'
            '    "skills_valoradas": ["Spark", "Databricks"]\n'
            "}\n"
            "```\n"
            "Genera siempre una respuesta que cumpla con este formato.")
    
    return prompt


def get_data_analyst_prompt():
    prompt = ("Analiza ofertas de trabajo para el puesto de 'Data Analyst' y responde con un JSON estructurado según los criterios especificados."
            "- Extrae elementos clave de la oferta relacionados con el nivel de inglés, experiencia, adecuación al rol de Data Analyst, y habilidades necesarias y valoradas.\n\n"
            "# Output Format\n"
            "Proporciona la respuesta en el siguiente formato JSON:\n"
            "```json\n"
            "{\n"
            '    "nivel_ingles": "[Marco europeo (A1, A2, B1, B2, C1, C2) o \'No especificado\'],"\n'
            '    "anios_experiencia": "[Número de años de experiencia requeridos o \'No especificado\'],"\n'
            '    "porcentaje": "[Porcentaje del 0 al 100],"\n'
            '    "skills_necesarias": ["[Lista de hard skills necesarias]"],\n'
            '    "skills_valoradas": ["[Lista de hard skills valoradas]"]\n'
            "}\n"
            "```\n\n"
            "# Steps\n"
            "1. **nivel_ingles:** Busca las menciones relacionadas con el inglés en la oferta. Traduce estas menciones al marco europeo adecuado. "
            "Indica 'No especificado' si no se menciona.\n"
            "2. **anios_experiencia:** Localiza cualquier mención al número de años de experiencia requerida. Deja 'No especificado' si no hay datos claros.\n"
            "3. **porcentaje:** Analiza la oferta de trabajo y compararla con el perfil típico de un data Analyst. Proporciona una evaluación objetiva que incluya una puntuación del 1 al 100, basada en cuánto encaja la oferta con las responsabilidades, habilidades y tecnologías características de un data analyst.\n"
            "4. **skills_necesarias:** Identifica y lista las hard skills exigidas. Excluye habilidades blandas.\n"
            "5. **skills_valoradas:** Haz una lista de las hard skills deseables pero no necesarias.\n\n"
            "# Notes\n"
            "- **Hard Skills:** Considera lenguajes de programación, herramientas, frameworks, bases de datos, técnicas de análisis o cualquier especificación tecnológica o metodológica.\n"
            "- **nivel_ingles:** Asegura que cada descripción del nivel de inglés se traduzca correctamente al equivalente en el marco europeo.\n"
            "- Proporciona una evaluación objetiva basada únicamente en la información proporcionada en la oferta.\n\n"
            "# Examples\n\n"
            "**Example 1**\n"
            "'Buscamos un Data Analyst con al menos 2 años de experiencia con inglés nivel Avanzado. Sus funciones serás: - Diseñar, desarrollar y ejecutar análisis de datos utilizando Python y SQL. - Crear visualizaciones dinámicas y reportes interactivos en Power BI. - Uso de tecnologías: Python, SQL, analítica de datos, machine Learning, Power BI, Azure, AWS y Spark.'\n\n"
            "**JSON resultante:**\n"
            "```json\n"
            "{\n"
            '    "nivel_ingles": "C1",\n'
            '    "anios_experiencia": "2",\n'
            '    "porcentaje": "90",\n'
            '    "skills_necesarias": ["Python", "Power BI", "SQL"],\n'
            '    "skills_valoradas": ["Azure", "AWS", "Spark", "Analítica de datos", "Machine Learning"]\n'
            "}\n"
            "```\n"
            "**Example 2**\n"
            "'Buscamos Analista Programador/a de bases de datos con experiencia en procesos ETL y experiencia de al menos 3 años y nivel medio de inglés- Experiencia en construcción de procesos ETL.- Manejo de bases de datos como Oracle, PostgreSQL y DuckDB.- Conocimientos de entornos Unix.- Planificación de trabajos en herramientas como Jenkins y Rundeck.- Experiencia en herramientas de control de versiones como Git.Tendrás PUNTOS EXTRA si tienes:- Experiencia en Python para el desarrollo de procesos ETL.- Experiencia en Django.- Experiencia en desarrollo de pequeñas aplicaciones web.'\n\n"
            "**JSON resultante:**\n"
            "```json\n"
            "{\n"
            '    "nivel_ingles": "B2",\n'
            '    "anios_experiencia": "3",\n'
            '    "porcentaje": "60",\n'
            '    "skills_necesarias": ["ETL", "Oracle", "PostgreSQL", "DuckDB", "Unix", "Jenkins", "Rundeck", "Git"],\n'
            '    "skills_valoradas": ["Python", "Django"]\n'
            "}\n"
            "```\n"
            "**Example 3**\n"
            "'Buscamos un Analista de Datos con : - Buen manejo de herramientas de análisis de datos, sistemas de almacenamiento, programación, Power BI, Power Apps y Tableau. Se valora conocimientos de Excel.- Experiencia mínima de 2 años en análisis de datos, valorándose positivamente haber realizado estas tareas en el sector Servicios. Es necesario un nivel básico de Inglés'\n\n"
            "**JSON resultante:**\n"
            "```json\n"
            "{\n"
            '    "nivel_ingles": "B1",\n'
            '    "anios_experiencia": "3",\n'
            '    "porcentaje": "80",\n'
            '    "skills_necesarias": ["Power BI", "Power Apps", "Tableau"],\n'
            '    "skills_valoradas": ["Excel"]\n'
            "}\n"
            "```\n"
            "Genera siempre una respuesta que cumpla con este formato.")
    
    return prompt

# Solo falta esta
def get_data_engineer_prompt():
    prompt = ("Analiza ofertas de trabajo para el puesto de 'Data Engineer' y responde con un JSON estructurado según los criterios especificados."
            "- Extrae elementos clave de la oferta relacionados con el nivel de inglés, experiencia, adecuación al rol de Data Engineer, y habilidades necesarias y valoradas.\n\n"
            "# Output Format\n"
            "Proporciona la respuesta en el siguiente formato JSON:\n"
            "```json\n"
            "{\n"
            '    "nivel_ingles": "[Marco europeo (A1, A2, B1, B2, C1, C2) o \'No especificado\'],"\n'
            '    "anios_experiencia": "[Número de años de expernecia requeridos o \'No especificado\'],"\n'
            '    "porcentaje": "[Porcentaje del 0 al 100],"\n'
            '    "skills_necesarias": ["[Lista de hard skills necesarias]"],\n'
            '    "skills_valoradas": ["[Lista de hard skills valoradas]"]\n'
            "}\n"
            "```\n\n"
            "# Steps\n"
            "1. **nivel_ingles:** Busca las menciones relacionadas con el inglés en la oferta. Traduce estas menciones al marco europeo adecuado. "
            "Indica 'No especificado' si no se menciona.\n"
            "2. **anios_experiencia:** Localiza cualquier mención al número de años de experiencia requerida. Deja 'No especificado' si no hay datos claros.\n"
            "3. **porcentaje:** Analiza la oferta de trabajo y compararla con el perfil típico de un data Engineer. Proporciona una evaluación objetiva que incluya una puntuación del 1 al 100, basada en cuánto encaja la oferta con las responsabilidades, habilidades y tecnologías características de un data engineer.\n"
            "4. **skills_necesarias:** Identifica y lista las hard skills exigidas. Excluye habilidades blandas.\n"
            "5. **skills_valoradas:** Haz una lista de las hard skills deseables pero no necesarias.\n\n"
            "# Notes\n"
            "- **Hard Skills:** Considera lenguajes de programación, herramientas, frameworks, bases de datos, técnicas de análisis o cualquier especificación tecnológica o metodológica.\n"
            "- **nivel_ingles:** Asegura que cada descripción del nivel de inglés se traduzca correctamente al equivalente en el marco europeo.\n"
            "- Proporciona una evaluación objetiva basada únicamente en la información proporcionada en la oferta.\n\n"
            "# Examples\n\n"
            "**Example 1**\n"
            "'Desde Boycor, buscamos un Data Engineer con al menos 3 años de experiencia y un nivel intermedio de inglés. ¿Cuál es la CLAVE de este puesto?:-Amplia experiencia en Python para desarrollo de procesos ETL y análisis de datos.-Experiencia trabajando con Spark para el procesamiento de grandes volúmenes de datos.-Experiencia en herramientas de orquestación como Airflow y plataformas de procesamiento como Databricks.- Valorable experiencia con Scala para procesamiento adicional de datos.- Conocimiento y experiencia en servicios de AWS (EC2, S3, Glue, Redshift, etc.), con especial enfoque en proyectos de migración.- Conocimientos sobre Cloudera y experiencia con arquitecturas basadas en Hadoop, incluyendo HBase y Hive.'\n\n"
            "**JSON resultante:**\n"
            "```json\n"
            "{\n"
            '    "nivel_ingles": "B2",\n'
            '    "anios_experiencia": "3",\n'
            '    "porcentaje": "100",\n'
            '    "skills_necesarias": ["Python", "ETL", "Spark", "Airflow", "Databricks", "AWS", "Cloudera", "Hadoop"],\n'
            '    "skills_valoradas": ["Scala"]\n'
            "}\n"
            "```\n"
            "**Example 2**\n"
            "'Buscamos FullStack Engineer con Experiencia: más de 3 años en soluciones FullStack (Java, Python, SQL, javascript, API Rest, Angular....) - Idiomas: inglés, necesaria soltura en interlocución verbal y escrita con equipos y clientes internacionales.- Conocimiento deseable: tecnologías semánticas (RDF, OWL, SPARQL, SHACL....)'\n\n"
            "**JSON resultante:**\n"
            "```json\n"
            "{\n"
            '    "nivel_ingles": "C1",\n'
            '    "anios_experiencia": "3",\n'
            '    "porcentaje": "50",\n'
            '    "skills_necesarias": ["Python", "Java", "SQL", "Javascript", "API Rest", "Angular"],\n'
            '    "skills_valoradas": ["RDF","OWL","SPARQL","SHACL"]\n'
            "}\n"
            "```\n"
            "```\n"
            "**Example 3**\n"
            "'Buscamos un Data Scientist Senior - Mínimo 4 años de experiencia en análisis de datos, programación en lenguaje Python. Pandas, SciPy, SciKit, statsmodels, imblearn, NumPy, etc..- Conocimientos avanzados de Machine Learning y herramientas de visualización como PowerBI.- Deseable familiaridad con SQL, NoSQL y AWS (deseable). - Buen nivel de inglés (hablado y escrito).'\n\n"
            "**JSON resultante:**\n"
            "```json\n"
            "{\n"
            '    "nivel_ingles": "B2",\n'
            '    "anios_experiencia": "4",\n'
            '    "porcentaje": "70",\n'
            '    "skills_necesarias": ["Python", "Pandas", "SciPy", "SciKit", "Statsmodels", "Imblearn", "NumPy", "Machine Learning", "PowerBI"],\n'
            '    "skills_valoradas": ["SQL", "NoSQL", "AWS"]\n'
            "}\n"
            "```\n"
            "Genera siempre una respuesta que cumpla con este formato.")
    
    return prompt