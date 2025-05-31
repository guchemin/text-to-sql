from ollama import Client
import re

# Inicializa cliente para Ollama local
client = Client(host='http://localhost:11434')

# Esquema do banco de dados
schema = """
Tabela: funcionarios
Colunas:
- id (inteiro)
- nome (texto)
- cargo (texto)
- departamento (texto)
- salario (float)
"""

# Entrada do usuário em linguagem natural
pergunta = input("Digite sua pergunta em linguagem natural: ")

# Geração do prompt
prompt = f"""
Você é um especialista em banco de dados SQL.

Baseado no seguinte schema:

{schema}

Responda APENAS com a consulta SQL, SEM explicações, SEM passos intermediários, SEM texto adicional, SEM tags <think>.

Pergunta: "{pergunta}"
"""


# Envia para o modelo Qwen via Ollama
resposta = client.chat(
    model='qwen3:0.6b',
    messages=[{'role': 'user', 'content': prompt}]
)

conteudo = resposta['message']['content']
conteudo_limpo = re.sub(r'<think>.*?</think>', '', conteudo, flags=re.DOTALL).strip()

# Exibe resultado
print("\n🔎 SQL gerada:")
print(conteudo_limpo)
