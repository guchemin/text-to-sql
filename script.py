from ollama import Client
import re

import pandas as pd
import psycopg2
import pymysql

# Inicializa cliente para Ollama local
client = Client(host='http://localhost:11434')
db_engine = input("Se você deseja utilizar mySQL digite 'mysql', se deseja utilizar PostgreSQL digite 'postgresql': ").strip().lower()
if db_engine not in ['mysql', 'postgresql']:
    raise ValueError("Por favor, escolha 'mysql' ou 'postgresql'.")
# Conexão com o banco de dados
if db_engine == 'postgresql':
    db = psycopg2.connect(
        host='localhost',
        database='university',
        user=input("Digite o seu nome de usuário: "),
        password=input("Digite a senha do banco de dados: ")
    )
else:
    db = pymysql.connect(
        host='localhost',
        user=input("Digite o seu nome de usuário: "),
        password=input("Digite a senha do banco de dados: "),
        database='university'
    )

# Esquema do banco de dados
cursor = db.cursor()
schema_parts = []

if db_engine == 'postgresql':
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
    tables = [row[0] for row in cursor.fetchall()]
    
    for table in tables:
        schema_parts.append(f"Tabela: {table}")
        cursor.execute(f"""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_schema='public' AND table_name='{table}'
            ORDER BY ordinal_position
        """)
        columns = cursor.fetchall()
        for col_name, col_type in columns:
            schema_parts.append(f"  - {col_name}: {col_type}")
        schema_parts.append("")  

else:  # MySQL
    cursor.execute("SHOW TABLES")
    tables = [row[0] for row in cursor.fetchall()]
    
    for table in tables:
        schema_parts.append(f"Tabela: {table}")
        cursor.execute(f"DESCRIBE {table}")
        columns = cursor.fetchall()
        for col in columns:
            schema_parts.append(f"  - {col[0]}: {col[1]}")
        schema_parts.append("")

schema = "\n".join(schema_parts)


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
# Executa a consulta SQL no banco de dados

try:
    cursor = db.cursor()
    cursor.execute(conteudo_limpo)
    resultados = cursor.fetchall()

    # Exibe os resultados
    print("\nResultados da consulta:")
    for linha in resultados:
        print(linha)
except psycopg2.Error as e:
    print(f"Erro ao executar a consulta SQL: {e}")
finally:
    # Fecha o cursor e a conexão
    if cursor:
        cursor.close()
    if db:
        db.close()

