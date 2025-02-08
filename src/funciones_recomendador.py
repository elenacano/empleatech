import pandas as pd # type: ignore
from sklearn.metrics.pairwise import cosine_similarity # type: ignore
from sklearn.feature_extraction.text import CountVectorizer # type: ignore
import seaborn as sns # type: ignore
import matplotlib.pyplot as plt # type: ignore

from src import funciones_bbdd as f_bbdd

def matriz_skills_ofertas():
    """
    Crea un DataFrame que combina los datos de dos colecciones de ofertas de empleo 
    (LinkedIn e InfoJobs) y desempaqueta la columna de transformación.

    Returns:
        pd.DataFrame: DataFrame combinado y transformado con la información de las ofertas.
        None: Si no se encuentran datos en la base de datos.
    """
   
    dic_ofertas = f_bbdd.obtener_todos_los_datos()

    if dic_ofertas is None:
        return None

    # Concatenamos los datos de las dos colecciones
    df_ofertas = pd.concat([pd.DataFrame(dic_ofertas["linkedin"]), pd.DataFrame(dic_ofertas["infojobs"])]).reset_index(drop=True)

    # Desempaquetamos la columna con los datos de la descripcion
    df_desempaquetado = pd.json_normalize(df_ofertas['transformacion'])
    df = pd.concat([df_ofertas.drop(columns=['transformacion']), df_desempaquetado], axis=1)

    print("\nMatriz de habilidades creada correctamente.")

    return df



def matriz_skills_ofertas_mas_usuario(lista_skills_usuario):
    """
    Amplía el DataFrame de ofertas con una fila adicional que representa las habilidades 
    del usuario y crea una columna combinada de habilidades necesarias y valoradas.

    Args:
        lista_skills_usuario (list): Lista de habilidades del usuario.

    Returns:
        pd.DataFrame: DataFrame actualizado con las habilidades del usuario y la columna combinada.
    """

    df = matriz_skills_ofertas()

    # Crear un diccionario con los valores de la nueva fila
    nueva_fila = {
        "_id": 0,
        "empleo": None,
        "plataforma": None,
        "titulo_oferta": None,
        "empresa": None,
        "fecha_publicacion": None,
        "tipo_empleo": None,
        "url_oferta": None,
        "descripcion": None,
        "min_salario": None,
        "max_salario": None,
        "nivel_ingles": None,
        "anios_experiencia": None,
        "porcentaje": None,
        "skills_necesarias": lista_skills_usuario,
        "skills_valoradas": [],
    }
    df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)

    df['skills_combinadas'] = df.apply(
        lambda row: ', '.join(row['skills_necesarias'] + row['skills_valoradas']),
        axis=1)

    return df


def vectorizacion_y_similitud(df):
    """
    Calcula la similitud coseno entre las ofertas de empleo y las habilidades del usuario 
    utilizando una representación vectorial basada en las habilidades combinadas.

    Args:
        df (pd.DataFrame): DataFrame que contiene las ofertas de empleo y sus habilidades.

    Returns:
        list: Lista de ofertas ordenadas por similitud con las habilidades del usuario. 
              Cada elemento es una tupla (índice de la oferta, valor de similitud).
    """

    vectorize = CountVectorizer(max_features=1000, stop_words='english')
    X = vectorize.fit_transform(df["skills_combinadas"]).toarray()

    # Calculamos las distancias a las ofertas
    similarity = cosine_similarity(X)
    ofertas_similares = list(enumerate(similarity[-1]))

    # Ofertas ordenadas que mejor se ajustan al perfil del usuario
    ofertas_ordenadas = sorted(ofertas_similares, key=lambda x: x[1], reverse=True)[1:]
    return ofertas_ordenadas


def get_empleo(index, df):
    """
    Obtiene los detalles de una oferta de empleo específica a partir de su índice.

    Args:
        index (int): Índice de la oferta en el DataFrame.
        df (pd.DataFrame): DataFrame que contiene las ofertas de empleo.

    Returns:
        dict: Diccionario con los detalles de la oferta de empleo (título, URL, habilidades necesarias y valoradas).
    """
    
    empleo = {}
    empleo["empleo"] = df[df.index==index]["empleo"].values[0]
    empleo["plataforma"] = df[df.index==index]["plataforma"].values[0]
    empleo["titulo_oferta"] = df[df.index==index]["titulo_oferta"].values[0]
    empleo["empresa"] = df[df.index==index]["empresa"].values[0]
    empleo["fecha_publicacion"] = df[df.index==index]["fecha_publicacion"].values[0]
    empleo["tipo_empleo"] = df[df.index==index]["tipo_empleo"].values[0]
    empleo["descripcion"] = df[df.index==index]["descripcion"].values[0]
    empleo["min_salario"] = df[df.index==index]["min_salario"].values[0]
    empleo["max_salario"] = df[df.index==index]["max_salario"].values[0]
    empleo["nivel_ingles"] = df[df.index==index]["nivel_ingles"].values[0]
    empleo["anios_experiencia"] = df[df.index==index]["anios_experiencia"].values[0]
    empleo["porcentaje"] = df[df.index==index]["porcentaje"].values[0]
    empleo["url_oferta"] = df[df.index==index]["url_oferta"].values[0]
    empleo["skills_necesarias"] = df[df.index==index]["skills_necesarias"].values[0]
    empleo["skills_valoradas"] = df[df.index==index]["skills_valoradas"].values[0]
    return empleo


def detalles_ofertas_recomendades(ofertas_recomendadas, df, grafico=True):
    """
    Genera una lista de detalles de las ofertas recomendadas y, opcionalmente, 
    crea un gráfico de barras con las similitudes de las 10 ofertas más cercanas.

    Args:
        ofertas_recomendadas (list): Lista de ofertas recomendadas con sus valores de similitud.
        df (pd.DataFrame): DataFrame que contiene las ofertas de empleo.
        grafico (bool, opcional): Indica si se debe generar un gráfico de barras. Por defecto es True.

    Returns:
        list: Lista de diccionarios con los detalles de las ofertas recomendadas.
    """
    
    lista_detalles_ofertas = []
    top_10_similar_offers = {}
    dic_claves = {}

    for elem in ofertas_recomendadas:

        empleo = get_empleo(elem[0], df)

        # En caso de que se haya coldo una fila de None
        if empleo["titulo_oferta"]==None or empleo["empresa"]==None:
            continue

        titulo_oferta = " ".join(empleo["titulo_oferta"].split())
        empresa = " ".join(empleo["empresa"].split())
        clave = (titulo_oferta, empresa)

        if clave in dic_claves.keys():
            continue

        else:
            dic_claves[clave]=empleo
            lista_detalles_ofertas.append(empleo)

            if len(top_10_similar_offers) < 10:
                top_10_similar_offers[empleo["titulo_oferta"]] = round(float(elem[1]),2)


        
    if grafico:
        plt.figure(figsize=(10, 6))

        # Crear gráfico de barras
        sns.barplot(
            x=list(top_10_similar_offers.values()), 
            y=list(top_10_similar_offers.keys()), 
            palette="mako"
        )

        # Añadir etiquetas y título
        plt.title(f"Top Ofertas", fontsize=16, pad=20)
        plt.xlabel("Similitud", fontsize=12)
        plt.ylabel("Oferta", fontsize=12)

    return lista_detalles_ofertas

def recomendador_hard_skills(skills_usuario):

    df = matriz_skills_ofertas_mas_usuario(skills_usuario)
    ofertas_recomendadas = vectorizacion_y_similitud(df)
    lista_detalles_ofertas = detalles_ofertas_recomendades(ofertas_recomendadas, df, False)

    return lista_detalles_ofertas


def recomendador(anios_experiencia, nivel_ingles, empleo, skills_usuario):
    lista_ofertas = recomendador_hard_skills(skills_usuario)
    min_exp, max_exp = anios_experiencia
    ofertas_filtradas = []
    
    for oferta in lista_ofertas:

        flag = 0
        
        # Si hay alguna oferta vacia que no la incluya
        if oferta["titulo_oferta"]==None or oferta["descripcion"]==None:
            continue

        if len(oferta["skills_necesarias"])== 0 and len(oferta["skills_valoradas"])== 0:
            continue

        # Comprobamos si la oferta piden alguna de las skills que tiene el usuario
        for skill in skills_usuario:
            if (skill in oferta["skills_necesarias"]) or (skill in oferta["skills_valoradas"]):
                flag = 1 
                break

        if flag == 0:
            continue
        
        exp_requerida = oferta["anios_experiencia"]
        if exp_requerida != "No especificado":
            try:
                exp_requerida = int(exp_requerida)
                if not (min_exp <= exp_requerida <= max_exp):
                    continue  
            except ValueError:
                continue 

        # Filtrar por nivel de inglés (aceptar "No especificado" o nivel adecuado)
        nivel_requerido = oferta["nivel_ingles"]
        if nivel_requerido != "No especificado":
            niveles_ingles = ["A1", "A2", "B1", "B2", "C1", "C2"]
            if niveles_ingles.index(nivel_requerido) > niveles_ingles.index(nivel_ingles):
                continue  # Nivel de inglés superior al del usuario

        # Filtrar por empleo (si no es "Todos", aplicar filtro)
        if empleo != "Todos":
            empleos_validos = ["data_analyst", "data_science", "data_engineer"]
            if oferta["empleo"] not in empleos_validos or oferta["empleo"] != empleo:
                continue

        # Si pasa todos los filtros, agregar a la lista de resultados
        ofertas_filtradas.append(oferta)

    return ofertas_filtradas

def metrica_recomendador(lista_recomendaciones, skills_usuario):
    puntuaciones = []

    for oferta in lista_recomendaciones:
        skills_oferta = oferta["skills_necesarias"]+oferta["skills_valoradas"]
        len_skills = len(skills_oferta)
        len_skills_oferta_y_usuario = 0

        for skill_usr in skills_usuario:
            if skill_usr in skills_oferta:
                len_skills_oferta_y_usuario += 1
        
        porc = 100*len_skills_oferta_y_usuario/len_skills
        puntuaciones.append(round(porc, 2))

        # print(oferta)
        # print(skills_oferta)
        # print(skills_usuario)
        # print(len_skills_oferta_y_usuario)
        # print(porc)
    
    return puntuaciones