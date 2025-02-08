#from readline import redisplay
import plotly.express as px # type: ignore
import plotly.graph_objects as go # type: ignore
from plotly.subplots import make_subplots # type: ignore
from collections import Counter
import seaborn as sns # type: ignore
import pandas as pd # type: ignore
import numpy as np

def empleo_por_plataforma(df):  
    mi_paleta_colores = ['#C70039', '#3b6684']  
    fig = px.histogram(df, 
                   x="empleo", 
                   color="plataforma", 
                   barmode="group", 
                   title="Distribución de Empleos por Plataforma",
                   labels={"empleo": "Tipo de empleo", "count": "Cantidad", "plataforma": "Plataforma"},
                   color_discrete_sequence=mi_paleta_colores,
                   text_auto=True  # Muestra automáticamente el texto sobre las barras
                  )

# Mostrar la figura
    fig.show()


def pies_empleo_plataforma(df):
       mi_paleta_colores = ['#C70039', '#3b6684']

       # Crear un subplot con 1 fila y 2 columnas
       fig = make_subplots(rows=1, cols=2, 
                     subplot_titles=("Distribución por plataforma", "Distribución por tipo de empleo"), 
                     specs=[[{'type': 'pie'}, {'type': 'pie'}]])

       # Primer gráfico de pastel (Distribución por plataforma)
       fig.add_trace(go.Pie(labels=df['plataforma'].value_counts().index, 
                            values=df['plataforma'].value_counts().values,
                            name='Plataforma', 
                            marker=dict(colors=mi_paleta_colores),
                            showlegend=False),  # Quitar leyenda del primer gráfico
                     row=1, col=1)

       # Segundo gráfico de pastel (Distribución por tipo de empleo)
       fig.add_trace(go.Pie(labels=df['empleo'].value_counts().index, 
                            values=df['empleo'].value_counts().values,
                            name='Tipo de empleo', 
                            marker=dict(colors=px.colors.qualitative.Set2),),
                     row=1, col=2)

       # Actualizar el layout para un diseño limpio
       fig.update_layout(title_text="Distribución por plataforma y tipo de empleo",
                     showlegend=True)

       # Mostrar el gráfico
       fig.show()


def top_empresas(df, top=20):
    # Contar las frecuencias de las empresas y obtener el top 10
    empresa_counts = df['empresa'].value_counts().head(top)

    # Crear el gráfico de barras
    fig = go.Figure(data=[go.Bar(
        x=empresa_counts.index,  # Las empresas
        y=empresa_counts.values,  # El conteo de cada empresa
        marker=dict(color='#C70039'),  # Puedes personalizar el color
        text=empresa_counts.values,  # Añadir los valores encima de las barras
        textposition='inside',
    )])

    # Títulos y etiquetas
    fig.update_layout(
        title="Top 20 empresas con más ofertas publicadas",
        xaxis_title="Empresa",
        yaxis_title="Número de empleos",
        showlegend=False  # Si no deseas la leyenda
    )

    # Mostrar el gráfico
    fig.show()


def tipo_empleo(df):
    empleo_counts = df['tipo_empleo'].value_counts()

    # Crear el gráfico de barras
    fig = go.Figure(data=[go.Bar(
        x=empleo_counts.index,  # Los tipos de empleo
        y=empleo_counts.values,  # El conteo de cada tipo de empleo
        marker=dict(color='#3b6684'),  # Puedes personalizar el color
        text=empleo_counts.values,  # Añadir los valores encima de las barras
    )])

    # Títulos y etiquetas
    fig.update_layout(
        title="Conteo por tipo de empleo",
        xaxis_title="Tipo de empleo",
        yaxis_title="Número de empleos",
        showlegend=False  # Si no deseas la leyenda
    )

    # Mostrar el gráfico
    fig.show()


def skills_por_empleo(df, empleo=''):


    # Unir ambas columnas de habilidades en una sola lista

    if empleo == '':
        df_aux = df
    
    elif empleo == 'analyst':
        df_aux = df[df['empleo'] == 'data_analyst']

    elif empleo == 'science':
        df_aux = df[df['empleo'] == 'data_science']

    elif empleo == 'engineer':
        df_aux = df[df['empleo'] == 'data_engineer']

    else:
        return

    all_skills = df_aux['skills_valoradas'].explode().dropna().tolist() + df_aux['skills_necesarias'].explode().dropna().tolist()

    # Contar la frecuencia de cada habilidad
    skills_counts = Counter(all_skills)

    # Ordenar las habilidades por frecuencia de manera descendente y obtener solo el top 20
    top_20_skills = sorted(skills_counts.items(), key=lambda x: x[1], reverse=True)[:20]

    # Crear el gráfico de barras
    fig = go.Figure(data=[go.Bar(
        x=[skill[0] for skill in top_20_skills],  # Habilidades ordenadas
        y=[skill[1] for skill in top_20_skills],  # Frecuencia de cada habilidad
        marker=dict(color='#3b6684'),  # Color de las barras
        text=[skill[1] for skill in top_20_skills],  # Mostrar el conteo sobre las barras
    )])

    # Títulos y etiquetas
    fig.update_layout(
        title=f"Skills más requeridas en ofertas de Data {empleo}",
        xaxis_title="Skills",
        yaxis_title="Frecuencia",
        showlegend=False  # Si no deseas la leyenda
    )

    # Mostrar el gráfico
    fig.show()


def skills_por_empleo_top10(df):
    empleos = {
        'Data Analyst': 'data_analyst',
        'Data Scientist': 'data_science',
        'Data Engineer': 'data_engineer'
    }

    # Crear subgráficos con 1 fila y 3 columnas
    fig = make_subplots(
        rows=1, cols=3, 
        subplot_titles=list(empleos.keys()), 
        shared_yaxes=True  # Compartir el eje Y para comparación
    )

    colores = ['#C70039', '#3b6684', '#374f1d']  # Colores para cada rol

    for i, (titulo, empleo) in enumerate(empleos.items(), start=1):
        # Filtrar por empleo
        df_aux = df[df['empleo'] == empleo]

        # Unir y contar las skills
        all_skills = df_aux['skills_valoradas'].explode().dropna().tolist() + df_aux['skills_necesarias'].explode().dropna().tolist()
        skills_counts = Counter(all_skills)

        # Obtener el top 10 de habilidades más demandadas
        top_10_skills = sorted(skills_counts.items(), key=lambda x: x[1], reverse=True)[:10]

        # Agregar la gráfica de barras al subplot correspondiente
        fig.add_trace(
            go.Bar(
                x=[skill[0] for skill in top_10_skills],
                y=[skill[1] for skill in top_10_skills],
                marker=dict(color=colores[i-1]),  # Asignar color distinto a cada gráfico
                text=[skill[1] for skill in top_10_skills],
                textposition='outside'  # Mostrar los valores sobre las barras
            ),
            row=1, col=i
        )

    # Ajustes finales del layout
    fig.update_layout(
        title="Top 10 Skills más demandadas en cada empleo",
        height=500, width=1200,
        showlegend=False
    )

    fig.show()


def niveles_ingles(df):
    # Contar la frecuencia de cada nivel de inglés
    nivel_ingles_counts = df['nivel_ingles'].value_counts()
    
    # Calcular el porcentaje de cada nivel
    total = nivel_ingles_counts.sum()
    porcentajes = (nivel_ingles_counts / total * 100).round(1)  # Redondear a 1 decimal
    etiquetas_texto = [f"{valor} ({porcentaje}%)" for valor, porcentaje in zip(nivel_ingles_counts.values, porcentajes)]

    # Crear un gráfico de barras con Plotly
    fig = px.bar(
        x=nivel_ingles_counts.index,  # Niveles de inglés
        y=nivel_ingles_counts.values,  # Frecuencia
        text=etiquetas_texto,  # Mostrar el número y porcentaje sobre las barras
        title="Distribución de los niveles de inglés requeridos",
        labels={'x': 'Nivel de Inglés', 'y': 'Frecuencia'},
        color_discrete_sequence=['#3b6684']  # Aplicar el color personalizado
    )

    # Ajustar la posición del texto sobre las barras
    fig.update_traces(textposition='outside')

    # Mostrar la gráfica
    fig.show()


def estudio_salario(df):
    df_salarios = df[(df["min_salario"] != "No especificado") & (df["min_salario"].notna())]
    df_salarios["min_salario"] = df_salarios["min_salario"].str.replace(".", "").apply(lambda x: int(x[:-1]))
    df_salarios["max_salario"] = df_salarios["max_salario"].str.replace(".", "").apply(lambda x: int(x[:-1]))

    df_salarios = df_salarios[df_salarios["min_salario"]>300]
    
    print("Salario mínimo y máximo para puestos de Data:")
    display(df_salarios[["min_salario", "max_salario"]].describe().T) # type: ignore

    for empleo in df["empleo"].unique():
        nombre = empleo.split("_")[1]
        print(f"\nSalario mínimo y máximo para puestos de data {nombre}:")
        df_aux = df_salarios[df_salarios["empleo"]==empleo]
        display(df_aux[["min_salario", "max_salario"]].describe().T) # type: ignore



def grafica_anios_experiencia(df):
    counts = df["anios_experiencia"].value_counts().reset_index()
    counts.columns = ["Años de Experiencia", "Cantidad"]

    counts["Porcentaje"] = (counts["Cantidad"] / counts["Cantidad"].sum()) * 100

    fig = px.bar(
        counts, 
        x="Años de Experiencia", 
        y="Cantidad", 
        text=counts["Porcentaje"].apply(lambda x: f"{x:.1f}%"), 
        title="Cantidad y porcentaje de ofertas por años de experiencia",
        labels={"Cantidad": "Número de Ofertas", "Años de Experiencia": "Años Requeridos"},
    )

    fig.update_traces(textposition="outside")  # Coloca los porcentajes fuera de las barras

    fig.show()

def anios_sueldo(df):
    # Filtramos los datos que tienen salario especificado
    df_salarios = df[(df["min_salario"] != "No especificado") & (df["min_salario"].notna())]

    # Limpiar los valores de salario (eliminar puntos y convertir a enteros)
    df_salarios["min_salario"] = df_salarios["min_salario"].str.replace(".", "").apply(lambda x: int(x[:-1]))
    df_salarios["max_salario"] = df_salarios["max_salario"].str.replace(".", "").apply(lambda x: int(x[:-1]))

    # Filtramos los salarios irreales (por ejemplo, menores de 300€)
    df_salarios = df_salarios[df_salarios["min_salario"] > 300]

    # Convertir a string para evitar orden numérico incorrecto
    df_salarios["anios_experiencia"] = df_salarios["anios_experiencia"].astype(str)

    # Definir orden correcto
    orden_experiencia = ["No especificado", "1", "2", "3", "4", "5"]
    df_salarios["anios_experiencia"] = pd.Categorical(df_salarios["anios_experiencia"], categories=orden_experiencia, ordered=True)

    # Filtramos filas con valores NaN en salario o años de experiencia
    df_filtered = df_salarios.dropna(subset=["min_salario", "max_salario", "anios_experiencia"])

    # Crear gráfico de boxplot y forzar el orden en el eje X
    fig = px.box(
        df_filtered, 
        x="anios_experiencia", 
        y=["min_salario", "max_salario"], 
        title="Distribución de salarios por años de experiencia",
        labels={"value": "Salario (€)", "anios_experiencia": "Años de Experiencia"},
        category_orders={"anios_experiencia": orden_experiencia}  # FORZAR EL ORDEN AQUÍ
    )

    fig.show()