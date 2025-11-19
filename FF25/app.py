# pip install Flask google-generativeai openai python-dotenv
from openai import OpenAI
from dotenv import load_dotenv
from flask import Flask, request, render_template, jsonify
from google import genai
from google.genai import types
import os
from google.genai.errors import APIError, ServerError
import base64

load_dotenv()

app = Flask(__name__)

# --- CONFIGURAÇÃO DOS CLIENTES ---

# 1. Configura Cliente Gemini (Para o Chat)
# Recomendo usar os.environ["GEMINI_API_KEY"] em produção
client_gemini = genai.Client(api_key="AIzaSyBsF1YWR91MWDYK-b-geMUFk-uzHKcufhA") 

# 2. Configura Cliente OpenAI (Para Imagens)
# O client da OpenAI busca automaticamente a chave na variável de ambiente "OPENAI_API_KEY"
# Certifique-se de ter o arquivo .env com OPENAI_API_KEY=sk-...
client_openai = OpenAI() 


# --- CONSTANTES ---
CHAT_MODEL_GEMINI = "gemini-2.5-flash-preview-09-2025"
IMAGE_MODEL_OPENAI = "dall-e-3" # Modelo padrão para geração de imagem de alta qualidade da OpenAI

# Variáveis globais para histórico
base = "" 

# --- ROTAS DE PÁGINA (RETORNAM HTML) ---

@app.route("/", methods=["GET"])
def start():
    return render_template("start.html")

@app.route("/chat", methods=["GET"])
def chat_page():
    global base
    
    if not base:
        try:
            # Mantém o Gemini para gerar a apresentação inicial
            response = client_gemini.models.generate_content(
                model=CHAT_MODEL_GEMINI,
                contents="(seja um agente ambiental que fala sobre o tema da ODS 6 (Água Limpa e Saneamento) da onu sendo um consultor) e cumprimente explicando como vc pode falar com o cliente(uma apresentacao extremamente curta e rapida de no maximo 200 caracteries)" 
            )
            base = response.text
        except Exception as e:
            print(f"Erro ao gerar a base: {e}")
            base = "Olá! Ocorreu um erro ao carregar a apresentação. Como posso ajudar você hoje com a ODS 6 (Água)?"

    return render_template("index.html", base=base)

@app.route("/nos")
def nos():
    return render_template("nos.html")

# --- ROTAS DE API (RETORNAM JSON) ---

@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json()
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "Prompt é obrigatório"}), 400

    try:
        # Mantém o Gemini para a lógica de chat (texto)
        full_prompt = f"(seja um agente ambiental que fala sobre o tema da ODS 6 (Água Limpa e Saneamento) da onu sendo um consultor(responda com no maximo 400 caracteries)) {prompt} "
    
        response = client_gemini.models.generate_content(
            model=CHAT_MODEL_GEMINI,
            contents=full_prompt
        )
        
        return jsonify({"response_text": response.text})

    except (APIError, ServerError) as e:
        print(f"Erro na API Gemini (Chat JSON): {e}")
        return jsonify({"error": "Erro no servidor de IA. Tente novamente mais tarde."}), 503
    except Exception as e:
        print(f"Ocorreu um erro inesperado (Chat JSON): {e}")
        return jsonify({"error": "Ocorreu um erro inesperado."}), 500

# --- ROTA DE GERAÇÃO DE IMAGEM ---
@app.route("/generate-image", methods=["POST"])
def generate_image_route():
    data = request.get_json()
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "Prompt de imagem é obrigatório"}), 400

    try:
        print(f"Gerando imagem com OpenAI (DALL-E 3) para: {prompt}")

        # Chamada à API da OpenAI (DALL-E 3)
        response = client_openai.images.generate(
            model=IMAGE_MODEL_OPENAI,
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
            # 'b64_json' retorna a imagem codificada diretamente, evitando ter que baixar URL
            response_format="b64_json" 
        )

        # Pega o base64 da resposta
        if response.data:
            image_data_base64 = response.data[0].b64_json
            return jsonify({"image_base64": image_data_base64})
        else:
            return jsonify({"error": "A OpenAI não retornou dados de imagem."}), 500

    except Exception as e:
        print(f"Erro na API OpenAI (Imagem): {e}")
        # Verifica se o erro é relacionado a 'Safety system' (conteúdo bloqueado)
        if "safety" in str(e).lower() or "content_policy_violation" in str(e).lower():
             return jsonify({"error": "A descrição da imagem violou as políticas de conteúdo da OpenAI."}), 400
             
        return jsonify({"error": f"Erro ao gerar imagem: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)