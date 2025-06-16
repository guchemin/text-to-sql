import re

import pandas as pd
import psycopg2
import pymysql

import google.generativeai as genai
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configurar a API Key do Gemini
# Obtém a API Key da variável de ambiente
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("A variável de ambiente GOOGLE_API_KEY não está definida. Certifique-se de que o arquivo .env existe e contém a chave.")

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-1.5-pro-latest')

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
    """Gera a consulta SQL a partir da pergunta em linguagem natural e do schema usando Gemini."""
    
    # Esta nova estrutura de prompt é mais robusta
    prompt = f"""### INSTRUÇÕES ###
Você é um tradutor de linguagem natural para SQL altamente eficiente.
Sua única tarefa é retornar um código SQL bruto e executável, baseado no schema e na pergunta do usuário.
NUNCA adicione texto antes ou depois do código SQL.
NUNCA use formatação Markdown como ```sql.
NUNCA adicione explicações ou comentários.

### SCHEMA DO BANCO DE DADOS ###
{schema}

### EXEMPLOS DE RESPOSTA ###
Pergunta: "Quantos alunos existem no total?"
SQL: SELECT COUNT(*) FROM aluno;

Pergunta: "Mostre o nome de todos os cursos."
SQL: SELECT nome_curso FROM curso;

Pergunta: "liste todas as tabelas"
SQL: SHOW TABLES;

### TAREFA ATUAL ###
Pergunta: "{pergunta}"
SQL:"""

    response = model.generate_content(prompt)
    
    # Mesmo com o prompt forte, adicionamos uma camada de limpeza para garantir.
    try:
        sql_query = response.text.strip()
        # Remove potenciais marcações de código que o modelo pode adicionar
        sql_query = re.sub(r"```(sql)?", "", sql_query, flags=re.IGNORECASE)
        sql_query = sql_query.strip()
        return sql_query
    except Exception as e:
        print(f"Erro ao extrair texto da resposta do modelo: {e}")
        # Retorna a resposta bruta para depuração se houver um erro inesperado
        # na estrutura da resposta (o que é raro com generate_content)
        return response.candidates[0].content.parts[0].text if response.candidates else ""


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
    import getpass
    password = getpass.getpass("Digite a senha do banco de dados: ")
    
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
