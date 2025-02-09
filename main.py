import streamlit as st # type: ignore
import pandas as pd # type: ignore
import base64
from dotenv import load_dotenv # type: ignore

import sys
sys.path.append(".../src")

import src.funciones_bbdd as f_bbdd
import src.funciones_recomendador as f_recomendador


load_dotenv()

# Page settings
st.set_page_config(
    page_title="Empleatech",
    page_icon="❄️️",
    layout="wide",
)

st.config.set_option("theme.primaryColor", "#393550")
# st.config.set_option("theme.backgroundColor", "#EFEFEF")  # White background
# st.config.set_option("theme.secondaryBackgroundColor", "#EFEFEF")  # Light gray sidebar


@st.cache_data
def obtener_datos():
    return f_bbdd.obtener_todos_los_datos()


datos = obtener_datos()
diccionario_skills_categorizadas = datos["skills_categorizadas"]


# Aplicar estilos personalizados
st.markdown(
    """
    <style>

    /* -------- Cambia el color del header para que no quede arriba una franja blanca -------- */
    .st-emotion-cache-12fmjuu {
        position: fixed;
        top: 0px;
        left: 0px;
        right: 0px;
        height: 3.75rem;
        background: #002631;
        outline: none;
        z-index: 999990;
        display: block;
    }

    /* -------- Fondo general de la página -------- */
    body {
        margin: 0;
        padding: 0;
        background: #002631;
    }

    /* -------- Marco que envuelve el contenido principal -------- */
    .stApp {
        border-radius: 15px; /* Esquinas redondeadas */
        padding: 10px; /* Espaciado interno */
        /* background: linear-gradient(135deg, #d5eaf5, #ced7dc, #d5eaf5);  Fondo degradado dentro del marco */
        background: #ced7dc; /* Fondo degradado dentro del marco */
        margin: 60px auto; /* Separación del contenido con respecto al borde de la ventana */
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.2); /* Sombra para el marco */
        max-width: 1300px;
    }
    

    /* ------ Padding del main ------*/
    .st-emotion-cache-1jicfl2 {
        width: 100%;
        padding: 1rem 4rem 2rem;
        min-width: auto;
        max-width: initial;
        overflow: scroll;
    }
    @media (max-width: 768px) {
        .st-emotion-cache-1jicfl2 {
            padding: 0.5rem 1rem 1rem; /* Reduce el padding en móviles */
        }
    }

    /* ------ Otro padding del main ------*/
    .st-emotion-cache-1ibsh2c {
        width: 100%;
        padding: 1rem 3rem 6rem;
        max-width: initial;
        min-width: auto;
    }

    .st-emotion-cache-t1wise {
        width: 100%;
        padding: 1rem 3rem 1rem;
        max-width: initial;
        min-width: auto;
    }

    @media (max-width: 768px) {
        .st-emotion-cache-t1wise {
        width: 100%;
        padding: 1rem 1rem 1rem;
        max-width: initial;
        min-width: auto;
        }
    }

    /* ------ banner donde va la foto metida del logo ------ */
    .top-banner {
            display: flex;
            justify-content: center;
            align-items: center;
            background-color:#ced7dc;
            padding: 5px;
            height: 60px;
            width: 100%;
            margin:0px;
        }

    /* ------ estilo de la foto ------ */
    .top-banner img {
        height: 60px;
    }

    /* ------ estilo de la columna de la derecha ------ */
    .right-column {
        padding: 20px;
        border-radius: 10px;
        max-height: 600px;
        margin-top: 10px;
        overflow-y: auto;
    }

    /*  ------ estilo de cada una de las ofertas ------ */
    .job-card {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 10px;
    }

    /* ------ Boton de buscar ofertas ------ */
    .st-emotion-cache-1igbibe {
        display: inline-flex;
        -webkit-box-align: center;
        align-items: center;
        -webkit-box-pack: center;
        justify-content: center;
        font-weight: 400;
        padding: 0.25rem 0.75rem;
        border-radius: 0.5rem;
        min-height: 2.5rem;
        margin: 10px;
        line-height: 1.6;
        color: inherit;
        width: auto;
        cursor: pointer;
        user-select: none;
        background-color: rgb(255, 255, 255);
        border: 1px solid rgba(49, 51, 63, 0.2);
        border-color: #002631;
    }


    .job-card {
        border: 1px solid #ddd;
        padding: 15px;
        border-radius: 8px;
        background: #f9f9f9;
    }

    .job-content {
        display: flex;
        justify-content: space-between;
    }

    .job-details {
        flex: 1;
    }

    .job-skills {
        flex: 1;
        margin-left: 15px;
    }

    .job-skills ul {
        list-style: none;
        padding: 0;
    }

    h4 {
        font-family: "Source Sans Pro", sans-serif;
        font-weight: 600;
        font-size: 1.5rem;
        padding: 0.75rem 0px 1rem;
        margin: 0px;
        line-height: 1.2;
        color:#002631;
        text-decoration: underline #002631;
    }


    /* ------------- Los headers de cada oferta -------------*/
    .st-emotion-cache-1104ytp h4 {        
        font-family: "Source Sans Pro", sans-serif;
        font-weight: 600;
        line-height: 1.2;
        margin: 0px;
        color:#002631;
        text-decoration: underline #002631;
    }

    .lupa-ofertas{
        height: 500px;
        display: flex;
        flex-direction: column; /* Asegura que los elementos se apilen en columna */
        justify-content: center; /* Centra verticalmente */
        align-items: center; /* Centra horizontalmente */
        text-align: center;
        border: 2px solid rgba(49, 51, 63, 0.2);
        color: #002631;
        border-radius: 30px;
        margin-top:10px;
        background-color:#e4edf5;
        padding:20px;
    }

    .centered-button {
        display: flex;
        justify-content: center;
        align-items: center;
    }

    @media (max-width: 768px) {
        .lupa-ofertas h3 {
            font-size: 1.5rem; /* Ajustar tamaño específico de h4 dentro de una clase */
        }
        .lupa-ofertas h6 {
            font-size: 1rem; /* Ajustar tamaño específico de h4 dentro de una clase */
        }
        .lupa-ofertas h7 {
            font-size: 0.9rem; /* Ajustar tamaño específico de h4 dentro de una clase */
        }
        .lupa-ofertas{
            height: 350px;
        }
        p{
            font-size: 1rem;
        }
        .job-card h4 {
            font-size: 1.2rem;
        }
        .job-card p {
            font-size: 0.9rem;
        }
        .job-skills {
            font-size: 0.9rem;
        }
        .job-skills ul {
            font-size: 0.9rem;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)



def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

logo_base64 = get_base64_image("imagenes/logo.png")

# Insertar la imagen como un banner en HTML
st.markdown(
    f"""
    <div class="top-banner">
        <img src="data:image/png;base64,{logo_base64}" alt="Empleatech Logo">
    </div>
    """,
    unsafe_allow_html=True
)


col1, col2 = st.columns([1, 2])


# -------------------- Parte de los filtros --------------------
with col1:
    
    st.markdown('<div class="left-column">', unsafe_allow_html=True)
    
    exp_min, exp_max = st.slider("Seleccione su rango de años de experiencia laboral:", min_value=0, max_value=15, value=(0, 5))

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        nivel_ingles = st.selectbox("Nivel de inglés", ["A1", "A2", "B1", "B2", "C1", "C2"], index=0, key="nivel_ingles")
    with col_f2:
        rol_seleccionado = st.selectbox("Rol deseado", ["Todos", "Data Science", "Data Engineer", "Data Analyst"], key="rol_seleccionado")



    st.write("Hard Skills:")

    with st.container(height=300, border=True):
        for categoria, skills in diccionario_skills_categorizadas.items():
            st.markdown(f"**{categoria}**")
            col_A, col_B = st.columns(2)
            for i, skill in enumerate(skills):
                if i % 2 == 0:
                    with col_A:
                        st.checkbox(skill, key=f"skill_{categoria}_{i}")
                else:
                    with col_B:
                        st.checkbox(skill, key=f"skill_{categoria}_{i}")
            st.markdown("---")  # Separador entre categorías


    left, middle, right = st.columns([1, 2, 1])
    search = middle.button("Buscar ofertas")
            
            
    st.markdown('</div>', unsafe_allow_html=True)




# -------------------- Parte donde se ven las ofertas --------------------

with col2:

    right_column_content = '<div class="right-column">'
    
    if search:

        dic_empleos = {"Data Science": "data_science", "Data Engineer": "data_engineer", "Data Analyst": "data_analyst", "Todos": "Todos"}

        skills_seleccionadas = []
        for categoria, skills in diccionario_skills_categorizadas.items():
            for i, skill in enumerate(skills):
                if st.session_state.get(f"skill_{categoria}_{i}"):  
                    skills_seleccionadas.append(skill)

        print(exp_min, exp_max, nivel_ingles, dic_empleos[rol_seleccionado], skills_seleccionadas)
        job_offers = f_recomendador.recomendador((exp_min, exp_max), nivel_ingles, dic_empleos[rol_seleccionado], skills_seleccionadas)
        

        if len(job_offers) == 0:
            right_column_content += f'''    <div class="lupa-ofertas">
                                            <h3>No hay ofertas :(</h3>
                                            <h6>Lo sentimos, para los parámetros especificados no se han encontrado ofertas.</h6>
                                            <h6>Pruebe en unos días o ajuste otros parámetros.</h6>
                                        </div>
                                '''

        else:    
            for offer in job_offers:

                if offer["plataforma"] == "infojobs":
                    if offer["min_salario"] == "No especificado" or offer["max_salario"] == "No especificado":
                        salario_text = ''
                    else:
                        min_salario = offer.get("min_salario")
                        max_salario = offer.get("max_salario")
                        salario_text = f'<strong>Rango salarial:</strong> {min_salario} - {max_salario}' if not (pd.isna(min_salario) or pd.isna(max_salario)) else ''
                else:
                    salario_text = ''

                set_skills_oferta = set()
                for skill in offer["skills_necesarias"]:
                    set_skills_oferta.add(skill)
                for skill in offer["skills_valoradas"]:
                    set_skills_oferta.add(skill)
                
                right_column_content += f''' <div class="job-card">
                                                <a href="{offer['url_oferta']}"><h4>{offer["titulo_oferta"]}</h4></a>
                                                <div class="job-content">
                                                    <div class="job-details">
                                                        <p><strong>Empresa:</strong> {offer["empresa"]}
                                                        <br><strong>Años de experiencia:</strong> {offer["anios_experiencia"]}
                                                        <br><strong>Nivel de inglés:</strong> {offer["nivel_ingles"]}
                                                        <br>{salario_text}</p>
                                                    </div>
                                                    <div class="job-skills">
                                                        <strong>Habilidades requeridas:</strong>
                                                        <ul>
                                                            {str(set_skills_oferta).replace("{", "").replace("}", "").replace("'", "")}
                                                        </ul>
                                                    </div>
                                                </div>
                                                <details>
                                                    <summary>Ver descripción</summary>
                                                    <p>{offer["descripcion_original"]}</p>
                                                </details>
                                            </div>
                                            '''

    else:
        right_column_content += f'''    <div class="lupa-ofertas">
                                            <h3>No te adaptes, aquí las ofertas se adaptan a ti</h3>
                                            <h6>Ajusta los filtros y accede a ofertas diseñadas para tu perfil</h6>
                                            <br>
                                            <h7>La primera web en la que tú eres el protagonista</h7>
                                        </div>
                                '''
    
    right_column_content += '</div>'  # Cierra el contenedor principal
    
    st.markdown(right_column_content, unsafe_allow_html=True)