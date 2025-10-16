from flask import Flask, request, render_template, send_file
from google import genai
import os

app = Flask(__name__)

client = genai.Client(api_key="AIzaSyCe-Kag-CkPYZ5edOpi_ZyC3NkQILm6VDY")

cenario = ""
historia_atual = ""
pergunta_atual = ""
@app.route("/", methods=["GET", "POST"])
def index():
    global historia_atual, cenario, pergunta_atual

    if request.method == "POST":
        escolha = request.form.get("chat").strip()
        cenario = escolha
        prompt = f"(seja um agente ambiental que fala sobre o tema da da ODS 2(agua) da onu sendo um consultor(responda com no maximo 400 caracteries)) {cenario} "
   
        response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt  
        )
        historia_atual = response.text
        pergunta_atual = escolha

        
        
   


    elif request.method == "GET":
        response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents= "(seja um agente ambiental que fala sobre o tema da da ODS 2(agua) da onu sendo um consultor) e cumprimente explicando como vc pode falar com o cliente(uma apresentacao extremamente curta e rapida de no maximo 200 caracteries)"  
        )
        historia_atual = response.text


    return render_template("index.html", resposta=historia_atual, perguntar=pergunta_atual)



@app.route("/start.html")
def perguntar_nome():
    return send_file('start.html')

if __name__ == "__main__":
    app.run(debug=True)



