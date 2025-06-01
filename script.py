from ollama import Client
import re

import pandas as pd
import psycopg2
import pymysql

# Inicializa cliente para Ollama local
client = Client(host='http://localhost:11434')

def connect_db(db_engine, user, password, database_name='university'):
    """Conecta ao banco de dados especificado."""
    if db_engine == 'postgresql':
        db = psycopg2.connect(
            host='localhost',
            database=database_name,
            user=user,
            password=password
        )
    elif db_engine == 'mysql':
        db = pymysql.connect(
            host='localhost',
            user=user,
            password=password,
            database=database_name
        )
    else:
        raise ValueError("Motor de banco de dados inválido. Escolha 'mysql' ou 'postgresql'.")
    return db

def get_schema(db, db_engine):
    """Obtém o esquema do banco de dados."""
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
    cursor.close()
    return "\n".join(schema_parts)

def generate_sql(schema, pergunta):
    """Gera a consulta SQL a partir da pergunta em linguagem natural e do schema."""
    prompt = f"""
Você é um especialista em banco de dados SQL.

Baseado no seguinte schema:

{schema}

Responda APENAS com a consulta SQL, SEM explicações, SEM passos intermediários, SEM texto adicional, SEM tags <think>.

Responda sempre com uma consulta SQL válida, mesmo que seja uma pergunta sobre estrutura do banco de dados que você saiba responder, responda uma consulta SQL (exemplo: SHOW TABLES;).

Pergunta: "{pergunta}"
"""
    resposta = client.chat(
        model='qwen3:0.6b',
        messages=[{'role': 'user', 'content': prompt}]
    )
    conteudo = resposta['message']['content']
    conteudo_limpo = re.sub(r'<think>.*?</think>', '', conteudo, flags=re.DOTALL).strip()
    return conteudo_limpo

def execute_sql(db, sql_query):
    """Executa a consulta SQL e retorna os resultados com nomes das colunas."""
    current_cursor = db.cursor()
    current_cursor.execute(sql_query)
    resultados = current_cursor.fetchall()
    
    # Obtém os nomes das colunas
    colunas = []
    if current_cursor.description:
        colunas = [desc[0] for desc in current_cursor.description]
    
    current_cursor.close()
    return resultados, colunas

def main_loop():
    db_engine = input("Se você deseja utilizar mySQL digite 'mysql', se deseja utilizar PostgreSQL digite 'postgresql': ").strip().lower()
    user = input("Digite o seu nome de usuário: ")
    password = input("Digite a senha do banco de dados: ")
    
    try:
        db = connect_db(db_engine, user, password)
        print("Conectado ao banco de dados com sucesso!")
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return

    try:
        schema = get_schema(db, db_engine)
        print("\nEsquema do banco de dados:")
        print(schema)
    except Exception as e:
        print(f"Erro ao obter o schema: {e}")
        if db:
            db.close()
        return

    while True:
        pergunta = input("\nDigite sua pergunta em linguagem natural (ou 'sair' para terminar): ")
        if pergunta.lower() == 'sair':
            break

        try:
            sql_query = generate_sql(schema, pergunta)
            print("\n🔎 SQL gerada:")
            print(sql_query)

            resultados, colunas = execute_sql(db, sql_query)
            print("\nResultados da consulta:")
            if resultados:
                if colunas:
                    print(" | ".join(colunas))
                    print("-" * (len(" | ".join(colunas))))
                for linha in resultados:
                    print(" | ".join(str(item) for item in linha))
            else:
                print("Nenhum resultado encontrado.")
        
        except (psycopg2.Error, pymysql.Error) as e:
            print(f"Erro ao processar a consulta: {e}")
            # db.rollback() # Opcional
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")

    if db:
        db.close()
    print("Programa encerrado.")

if __name__ == "__main__":
    main_loop()

