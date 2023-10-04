# Lectura de Multiples Documentos Chatbot con Langchain y Streamlit

## Arquitectura de la aplicación

<p align=center>
<img src="src\arq.png" height = 460 weight=400>
<p>

- Carga de los documentos 
- Extracción del contenido 
- Se parte el contenido y se divide en segmentos
- Creación de embaddings para cada segmento 









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
