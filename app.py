from flask import Flask, request, jsonify, render_template
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Substitua pela sua chave de API
# É recomendável usar variáveis de ambiente (os.environ['GEMINI_API_KEY'])
client = genai.Client(api_key=os.getenv("KEY"))
model = 'gemini-2.5-flash' # Um bom modelo para essa tarefa de extração

@app.route('/', methods=['GET'])
def index():
    # Renderiza o seu template HTML com o formulário
    return render_template('index.html')

@app.route('/processar_emails', methods=['POST'])
def processar_emails():
    # Pega o texto do formulário HTML
    texto_concatenado = request.form.get('texto_emails')

    if not texto_concatenado:
        return jsonify({"erro": "Nenhum texto fornecido."}), 400

    # O Prompt é a parte crucial. Ele instrui o modelo a tarefa e o formato de saída.
    prompt = f"""
    O texto a seguir contém vários e-mails, possivelmente misturados com outros textos, 
    e eles estão concatenados em uma única string.
    
    Por favor, analise o texto e separe os emails com -----.
    
    NÃO inclua nenhuma explicação, texto adicional, ou formatação além dos emails separados com -----.
    
    TEXTO:
    ---
    {texto_concatenado}
    ---
    """

    try:
        # Chama a API do Gemini
        response = client.models.generate_content(
            model=model,
            contents=prompt
        )

        # A resposta deve ser uma string JSON (a lista de e-mails)
        # Usamos eval() com cuidado aqui, mas para JSON puro, é a forma mais direta de parsear o output do modelo.
        # Alternativamente, você pode usar json.loads() e tentar limpar o output antes.
        try:
             # Tentativa de parsear a string JSON para uma lista Python
             emails_extraidos = response.text.strip()
        except (SyntaxError, NameError):
             # Em caso de falha no parse, assumimos que o modelo pode ter retornado texto inesperado.
             # Você pode adicionar mais lógica de limpeza ou um prompt de 'reparo' aqui.
             return jsonify({
                 "sucesso": False, 
                 "mensagem": "Falha ao analisar a resposta do Gemini.",
                 "resposta_bruta": response.text.strip()
             }), 500


        return jsonify({
            "sucesso": True,
            "emails": emails_extraidos
        })

    except Exception as e:
        return jsonify({"sucesso": False, "erro": str(e)}), 500


@app.route('/classificar_emails', methods=['POST'])
def classificar_emails():
    # Pega o texto do formulário HTML
    texto_concatenado = request.form.get('emails_separados')

    if not texto_concatenado:
        return jsonify({"erro": "Nenhum texto fornecido."}), 400

    # O Prompt é a parte crucial. Ele instrui o modelo a tarefa e o formato de saída.
    prompt = f"""
    O texto a seguir contém vários e-mails, separados por -----.
    
    Por favor, analise os emails cada um individualmente e classifique cada em um dos emails em um desses dois tipos:

    -Tipo Produtivo: Emails que requerem uma ação ou resposta específica (ex.: solicitações de suporte técnico, atualização sobre casos em aberto, dúvidas sobre o sistema).

    -Tipo Improdutivo: Emails que não necessitam de uma ação imediata (ex.: mensagens de felicitações, agradecimentos).
    
    NÃO inclua nenhuma explicação, texto adicional, ou formatação além dos emails completos com suas classificaçôes.
    
    TEXTO:
    ---
    {texto_concatenado}
    ---
    """

    try:
        # Chama a API do Gemini
        response = client.models.generate_content(
            model=model,
            contents=prompt
        )

        # A resposta deve ser uma string JSON (a lista de e-mails)
        # Usamos eval() com cuidado aqui, mas para JSON puro, é a forma mais direta de parsear o output do modelo.
        # Alternativamente, você pode usar json.loads() e tentar limpar o output antes.
        try:
             # Tentativa de parsear a string JSON para uma lista Python
             emails_extraidos = response.text.strip()
        except (SyntaxError, NameError):
             # Em caso de falha no parse, assumimos que o modelo pode ter retornado texto inesperado.
             # Você pode adicionar mais lógica de limpeza ou um prompt de 'reparo' aqui.
             return jsonify({
                 "sucesso": False, 
                 "mensagem": "Falha ao analisar a resposta do Gemini.",
                 "resposta_bruta": response.text.strip()
             }), 500


        return jsonify({
            "sucesso": True,
            "emails": emails_extraidos
        })

    except Exception as e:
        return jsonify({"sucesso": False, "erro": str(e)}), 500


@app.route('/responder_emails', methods=['POST'])
def responder_emails():
    # Pega o texto do formulário HTML
    texto_concatenado = request.form.get('emails_classificados')

    if not texto_concatenado:
        return jsonify({"erro": "Nenhum texto fornecido."}), 400

    # O Prompt é a parte crucial. Ele instrui o modelo a tarefa e o formato de saída.
    prompt = f"""
    O texto a seguir contém vários e-mails, separados por ----- e classificados com um tipo.
    
    Por favor, analise os emails e o tipo de cada um individualmente e crie uma sugestão de resposta para cada e separe a sugestão do resto do email com ===== e comece com sua sugestão com 'Sugestão de Resposta:':
    
    NÃO inclua nenhuma explicação, texto adicional, ou formatação além dos email com suas classificaçôes e sugestões de resposta.
    
    TEXTO:
    ---
    {texto_concatenado}
    ---
    """

    try:
        # Chama a API do Gemini
        response = client.models.generate_content(
            model=model,
            contents=prompt
        )

        # A resposta deve ser uma string JSON (a lista de e-mails)
        # Usamos eval() com cuidado aqui, mas para JSON puro, é a forma mais direta de parsear o output do modelo.
        # Alternativamente, você pode usar json.loads() e tentar limpar o output antes.
        try:
             # Tentativa de parsear a string JSON para uma lista Python
             emails_extraidos = response.text.strip()
        except (SyntaxError, NameError):
             # Em caso de falha no parse, assumimos que o modelo pode ter retornado texto inesperado.
             # Você pode adicionar mais lógica de limpeza ou um prompt de 'reparo' aqui.
             return jsonify({
                 "sucesso": False, 
                 "mensagem": "Falha ao analisar a resposta do Gemini.",
                 "resposta_bruta": response.text.strip()
             }), 500


        return jsonify({
            "sucesso": True,
            "emails": emails_extraidos
        })

    except Exception as e:
        return jsonify({"sucesso": False, "erro": str(e)}), 500

if __name__ == '__main__':
    # Garante que você tenha um diretório 'templates' com seu 'index.html'
    app.run(debug=True)