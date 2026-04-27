# ArandaCalzadoBack
Proyecto API 

🚀 Pasos para correr el Backend (Aranda Calzado)
Abre tu terminal, asegúrate de estar ubicado en la raíz del proyecto (donde está el archivo requirements.txt) y ejecuta los siguientes comandos en orden:

1. Crear el entorno virtual (Esto creará una carpeta llamada venv que ya está ignorada en Git)

bash
python -m venv venv

2. Activar el entorno virtual

Si usas Windows:
bash
venv\Scripts\activate
Si usas Mac / Linux:
bash
source venv/bin/activate

3. Instalar las dependencias del proyecto

bash
pip install -r requirements.txt

4. Entrar a la carpeta del proyecto

bash
cd arandaCalzado

5. Preparar la base de datos local

bash
python manage.py migrate

6. Cargar los datos iniciales (Usuario Admin y Materiales base)

bash
python seed.py

7. Levantar el servidor

bash
python manage.py runserver
(El servidor quedará corriendo en http://localhost:8000/)
