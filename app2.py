import streamlit as st
import google.generativeai as genai
import PyPDF2
from PIL import Image
import base64
import os

# Configuración de la página
st.set_page_config(page_title="Tutor en línea", page_icon="🎓", layout="wide")

# Estilos CSS personalizados
st.markdown("""
<style>
    .header-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: linear-gradient(135deg, #6e48aa 0%, #9d50bb 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .header-text {
        flex: 1;
    }
    .header-image {
        width: 80px;
        height: 80px;
        margin-left: 1rem;
    }
    .question-input-container {
        margin-top: 1.5rem;
    }
    .answer-container {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        margin-top: 1.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# Función para convertir imagen local a base64
def get_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# Configurar la clave API de Google AI
genai.configure(api_key="AIzaSyDB8nfedASwDdg-xY4ZsFVeaxr1AzNPLgc")

# Cargar el modelo Gemini
model = genai.GenerativeModel('gemini-2.0-flash-exp')

# Cargar imagen local para el encabezado
header_image_path = "chatbot.png"  # Imagen para el título

try:
    # Convertir imagen a base64
    header_image_base64 = get_image_base64(header_image_path)
    
    # Título llamativo con imagen
    st.markdown(f"""
    <div class="header-container">
        <div class="header-text">
            <h1 style="color: white; margin: 0;">¿Cuál es tu duda sobre la formación?</h1>
            <p style="color: #f0f0f0; margin: 0;">Escribe tu NOMBRE con APELLIDOS para tener una búsqueda personalizada</p>
            <p style="color: #f0f0f0; margin: 0;">Escribe tu NOMBRE con APELLIDOS para tener una búsqueda personalizada</p>
        </div>
        <img src="data:image/png;base64,{header_image_base64}" class="header-image">
    </div>
    """, unsafe_allow_html=True)
    
except FileNotFoundError as e:
    st.error(f"Error al cargar la imagen: {e}. Asegúrate de tener el archivo 'header_icon.png' en el directorio.")
    # Mostrar título simple si no hay imagen
    st.markdown("""
    <div style="background: linear-gradient(135deg, #6e48aa 0%, #9d50bb 100%); padding: 1.5rem; border-radius: 10px; color: white; margin-bottom: 2rem;">
        <h1 style="color: white; margin: 0;">¿Cuál es tu duda académica?</h1>
        <p style="color: #f0f0f0; margin: 0;">Obtén respuestas personalizadas de nuestro sistema</p>
    </div>
    """, unsafe_allow_html=True)

# Campo de entrada para preguntas
with st.container():
    st.markdown('<div class="question-input-container">', unsafe_allow_html=True)
    user_query = st.text_input("Haz tu pregunta", 
                             label_visibility="hidden", 
                             placeholder="Escribe tu pregunta aquí...",
                             key="question_input")
    st.markdown('</div>', unsafe_allow_html=True)

def extract_text_from_pdf(pdf_path):
    """Extrae el texto de un PDF."""
    text = ""
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
    except Exception as e:
        print(f"Error al procesar el PDF: {e}")
        return None
    return text

def chat_with_gemini(pdf_text, user_query):
    """Chatea con Gemini usando el contexto del texto del PDF."""
    if not pdf_text:
        return "No se pudo extraer texto del PDF."

    prompt = f"Aquí tienes el contexto del PDF:\n\n{pdf_text}\n\nPregunta: {user_query}"
    try:
       response = model.generate_content(prompt)
       return response.text
    except Exception as e:
        return f"Error al interactuar con Gemini: {e}"

# Procesar el PDF y responder preguntas
pdf_text = extract_text_from_pdf("APDAEMMA.pdf")

if pdf_text and user_query:
    with st.spinner('Analizando tu consulta...'):
        answer = chat_with_gemini(pdf_text, user_query)
        print("Respuesta de Gemini:\n", answer)
        
        # Mostrar la respuesta en un contenedor con estilo
        st.markdown(f"""
        <div class="answer-container">
            <h3 style="color: #2c3e50; margin-top: 0;">Respuesta:</h3>
            <p style="color: #34495e; line-height: 1.6;">{answer}</p>
        </div>
        """, unsafe_allow_html=True)
