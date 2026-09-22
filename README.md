# Agente Ambiental (Capyrobot)

Experiência web interativa, com tema ambiental (ODS 6 — Água Limpa e Saneamento), que combina páginas HTML/CSS/JS no estilo "terminal retrô" com dois pequenos backends em Flask responsáveis por gerar áudio, texto e imagens por meio de IA generativa.

> **Sobre o nome:** apesar de o repositório se chamar "agente-ambiental", o projeto não realiza monitoramento de sensores ou coleta de dados ambientais reais. Trata-se de uma aplicação educativa/experimental sobre o tema da ODS 6 da ONU, construída como projeto de hackathon pela equipe "Capyrobot".

## Sobre o projeto

O repositório contém **duas aplicações Flask independentes**, cada uma com seu próprio conjunto de páginas:

1. **Aplicação raiz — "Mundo Perfeito"** (`app.py`, na raiz do projeto)
   Um fluxo guiado em que o usuário:
   - Informa o nome (`pergunta_nome.html`) e ouve uma saudação em áudio gerada por IA;
   - Descreve como imagina um "mundo perfeito" (`mundo_perfeito.html`);
   - Recebe uma imagem realista gerada por IA a partir dessa descrição, com foco em ambientes aquáticos (`resultado.html`).

2. **Aplicação `FF25/` — Chat "Capyrobot"** (`FF25/app.py`)
   Uma tela inicial (`start.html`) que leva a um chat (`chat.html`/`index.html` do Flask) no qual o usuário conversa com um agente de IA que atua como consultor sobre a ODS 6 (Água Limpa e Saneamento), podendo também alternar para um "modo imagem" e gerar ilustrações a partir de um prompt.

Ambas as aplicações possuem uma página "Sobre nós" (`nos.html`) apresentando a equipe do projeto.

## Funcionalidades

- Geração de áudio personalizado via texto-para-voz (rota fixa e rota personalizada com o nome do usuário).
- Geração de prompts de imagem enriquecidos por IA e criação da imagem final (modelo de imagem realista, com foco em cenários de água/natureza).
- Chat conversacional temático sobre água limpa e saneamento (ODS 6), com respostas curtas geradas por um modelo de linguagem.
- Geração de imagens dentro do próprio chat, a partir de um prompt digitado pelo usuário.
- Listagem das imagens já geradas e servidas como arquivos estáticos.
- Página "Sobre nós" com a equipe do projeto.

## Arquitetura e tecnologias

**Frontend**
- HTML5 + CSS3 (estilo "terminal retrô", sem framework de CSS)
- JavaScript puro (`fetch` para chamadas às rotas do backend, manipulação de áudio/imagem no DOM)
- Templates Jinja2 renderizados pelo Flask (`FF25/templates`) e páginas HTML estáticas servidas diretamente (raiz do projeto)

**Backend**
- Python 3 + [Flask](https://flask.palletsprojects.com/)
- [Flask-CORS](https://flask-cors.readthedocs.io/) (aplicação raiz)
- [python-dotenv](https://pypi.org/project/python-dotenv/) (aplicação `FF25/`)

**Integrações de IA**
- [OpenAI API](https://platform.openai.com/docs) — usada nas duas aplicações:
  - `gpt-4o-mini` para enriquecer prompts de imagem (aplicação raiz)
  - `dall-e-3` para geração de imagens (ambas as aplicações)
  - `tts-1` para geração de áudio (aplicação raiz)
- [Google Gen AI SDK](https://pypi.org/project/google-genai/) (pacote `google-genai`, importado como `from google import genai`) — modelo `gemini-2.5-flash-preview-09-2025` usado para o chat conversacional (aplicação `FF25/`)

## Rotas do backend

### Aplicação raiz (`app.py`) — porta 5000

| Rota | Método | Descrição |
|---|---|---|
| `/` | GET | Página inicial (`index.html`) |
| `/pergunta_nome.html` | GET | Tela para o usuário informar o nome |
| `/mundo_perfeito.html` | GET | Tela para descrever o "mundo perfeito" |
| `/resultado.html` | GET | Tela de resultado com a imagem gerada |
| `/nos` | GET | Página "Sobre nós" |
| `/imagem/<filename>` | GET | Serve uma imagem salva localmente |
| `/audio/<filename>` | GET | Serve um áudio salvo localmente |
| `/audio_pergunta` | GET | Serve o áudio fixo da pergunta do nome |
| `/audio_personalizado/<nome>` | GET | Gera (se necessário) e serve o áudio personalizado com o nome informado |
| `/imagens` | GET | Lista, em JSON, as imagens `.png` já geradas |
| `/gerar` | POST | Recebe `nome` e `mundo_perfeito`, gera o prompt enriquecido e a imagem final |

### Aplicação `FF25/app.py` — porta 5000

| Rota | Método | Descrição |
|---|---|---|
| `/` | GET | Página inicial do sistema (`start.html`) |
| `/chat` | GET | Página de chat, gera a apresentação inicial do agente |
| `/nos` | GET | Página "Sobre nós" |
| `/api/chat` | POST | Recebe `prompt` e retorna a resposta do agente conversacional |
| `/generate-image` | POST | Recebe `prompt` e retorna a imagem gerada em base64 |

> As duas aplicações usam a porta `5000` por padrão — não é possível rodá-las ao mesmo tempo sem alterar a porta de uma delas.

## Pré-requisitos

- Python 3.10+ (recomendado)
- `pip`
- Uma chave de API da [OpenAI](https://platform.openai.com/) (usada pelas duas aplicações)
- Uma chave de API do [Google AI Studio / Gemini](https://ai.google.dev/) (usada apenas pela aplicação `FF25/`)

## Como instalar e rodar

### 1. Clonar o repositório

```bash
git clone https://github.com/akira113p/agente-ambiental.git
cd agente-ambiental
```

### 2. Aplicação raiz — "Mundo Perfeito"

```bash
pip install flask flask-cors openai
```

Edite o arquivo `config.py` na raiz do projeto e preencha as suas credenciais da OpenAI:

```python
OPENAI_API_KEY = "sua-chave-aqui"
OPENAI_ORGANIZATION = "sua-organizacao-aqui"
```

Em seguida, execute:

```bash
python app.py
```

A aplicação sobe em `http://127.0.0.1:5000`.

### 3. Aplicação `FF25/` — Chat "Capyrobot"

```bash
cd FF25
pip install flask python-dotenv openai google-genai
```

Crie um arquivo `.env` dentro de `FF25/` com a sua chave da OpenAI:

```
OPENAI_API_KEY=sk-...
```

> **Atenção:** no código atual (`FF25/app.py`), a chave da API do Gemini está escrita diretamente no código-fonte (`genai.Client(api_key="...")`) em vez de ser lida de uma variável de ambiente. Antes de publicar ou reutilizar este projeto, recomenda-se remover essa chave do código e passá-la por uma variável de ambiente (por exemplo, `GEMINI_API_KEY`), além de revogar/gerar uma nova chave caso a atual já tenha sido exposta publicamente.

Em seguida, execute:

```bash
python app.py
```

A aplicação sobe em `http://127.0.0.1:5000`.

## Variáveis/credenciais utilizadas

- `OPENAI_API_KEY` — chave da API da OpenAI (usada pelas duas aplicações)
- `OPENAI_ORGANIZATION` — ID da organização OpenAI (usado pela aplicação raiz, via `config.py`)
- Chave da API do Google Gemini (usada pela aplicação `FF25/`; ver observação de segurança acima)

## Estrutura do projeto

```
agente-ambiental/
├── app.py                     # Backend Flask da aplicação "Mundo Perfeito"
├── config.py                  # Credenciais da OpenAI usadas por app.py
├── gerar_audio_personalizado.py  # Script de linha de comando para gerar áudio avulso
├── index.html                 # Tela inicial
├── pergunta_nome.html         # Tela de identificação do usuário
├── mundo_perfeito.html        # Tela de descrição do "mundo perfeito"
├── resultado.html             # Tela de resultado com a imagem gerada
├── nos.html                   # Página "Sobre nós"
├── imagens/                   # Imagens estáticas e imagens geradas pela IA
├── audios/                    # Áudios gerados (fixo e personalizados)
└── FF25/                      # Segunda aplicação: chat "Capyrobot"
    ├── app.py                 # Backend Flask do chat (Gemini + DALL-E 3)
    ├── templates/              # start.html, index.html (chat), nos.html
    └── static/
        ├── css/                # style.css, chat.css, nos.css, start.css
        ├── js/script.js        # Relógio, animação de abertura e lógica de UI
        └── imagens/            # Imagens estáticas da interface
```

## Licença

Este repositório não possui um arquivo de licença definido no momento.
