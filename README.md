# Lectura de Multiples Documentos Chatbot con Langchain y Streamlit

## Arquitectura de la aplicación

<p align=center>
<img src="src\arq.png" height = 460 weight=400>
<p>

- Carga de los documentos 
- Extracción del contenido 
- Se parte el contenido y se divide en segmentos
- Creación de embaddings para cada segmento 
- Construcción de la Semántica para generar la Base de Conocimiento  
- Cuando el usuario genere una pregunta se crean embeddings y una búsqueda semántica para encontrar similitudes en la Base de Conocimiento, luego de obtener las respuestas se clasificarán los resultados entrará al LLM y luego se dará la respuesta al usuario.

## Ejecución Local 💻

Siga estos pasos para configurar y ejecutar el proyecto localmente:

### Pre-requisitos
- Python 3.8 o superior
- Git

### Instalación
Clonar el repositorio :

`git clone https://github.com/carbajaljerson/ChatbotForDocLlamaLch.git`


Crear el entorno virtual :
```bash
$ python -m virtualenv env
$ source env/Scripts/activate
```

Instalar las dependencias en el ambiente virtual :

`pip install -r requirements.txt`


Lanzar el servicio localmente :

`streamlit run app.py`
