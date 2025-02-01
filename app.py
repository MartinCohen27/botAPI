from flask import Flask, render_template, request, jsonify
import openai
import os


# Cargar la clave de API desde una variable de entorno
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv(override=True)
api_key = os.getenv("OPENAI_API_KEY")

print("API Key cargada:", api_key)

# Inicializar el cliente de OpenAI
client = openai.OpenAI(api_key=api_key)


app = Flask(__name__)

# Configuración inicial del asistente
messages = [
    {"role": "system", "content": """Eres Martin, un asistente virtual de atención al cliente líder mundial para emprendedores y negocios...
    (Aquí sigue toda tu configuración original)"""}
]

# Carga de archivos
file_paths = [
    "D:/Martin/Testeo/Base_Datos_Cosmeticos_100.txt",
    "D:/Martin/Testeo/Informacion_Empresa_Cosmeticos.txt"
]

for file_path in file_paths:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            file_content = f.read()
            messages.append({"role": "system", "content": f"Usa esta información: {file_content}"})
    except FileNotFoundError:
        print(f"Advertencia: No se encontró el archivo {file_path}. Se omitirá.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"response": "No recibí un mensaje válido."})

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.2,
        max_tokens=800
    )

    assistant_response = response.choices[0].message.content.strip()
    messages.append({"role": "assistant", "content": assistant_response})

    return jsonify({"response": assistant_response})

if __name__ == '__main__':
    app.run(debug=True)