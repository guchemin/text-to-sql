import re
import pandas as pd
import psycopg2
import pymysql
import google.generativeai as genai
import os
from dotenv import load_dotenv
import getpass

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configurar a API Key do Gemini
# Obtém a API Key da variável de ambiente
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("A variável de ambiente GOOGLE_API_KEY não está definida. Certifique-se de que o arquivo .env existe e contém a chave.")

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-1.5-pro-latest')

# --- FUNÇÃO PARA LISTAR BANCOS DE DADOS ---
def list_databases(db_engine, user, password):
    """Conecta ao servidor e lista os bancos de dados disponíveis."""
    conn = None
    cursor = None
    db_list = []
    
    try:
        if db_engine == 'postgresql':
            conn = psycopg2.connect(host='localhost', dbname='postgres', user=user, password=password)
            conn.set_session(autocommit=True)
            cursor = conn.cursor()
            # Query para listar bancos de dados de usuário, excluindo templates
            cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false AND datname <> 'postgres';")
            db_list = [row[0] for row in cursor.fetchall()]
        
        elif db_engine == 'mysql':
            conn = pymysql.connect(host='localhost', user=user, password=password)
            cursor = conn.cursor()
            # Query para listar bancos de dados de usuário, excluindo os de sistema
            cursor.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name NOT IN ('information_schema', 'mysql', 'performance_schema', 'sys');")
            db_list = [row[0] for row in cursor.fetchall()]
            
    except (psycopg2.Error, pymysql.Error) as e:
        # Retorna o erro para ser tratado no loop principal
        raise e
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            
    return db_list

def connect_db(db_engine, user, password, database_name):
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
    colunas = []
    if current_cursor.description:
        colunas = [desc[0] for desc in current_cursor.description]
    current_cursor.close()
    return resultados, colunas

def main_loop():
    db_engine = input("Se você deseja utilizar mySQL digite 'mysql', se deseja utilizar PostgreSQL digite 'postgresql': ").strip().lower()
    user = input("Digite o seu nome de usuário: ")
    password = getpass.getpass("Digite a senha do banco de dados: ")
    
    # Bloco para listar e selecionar o banco de dados
    try:
        available_dbs = list_databases(db_engine, user, password)
        if not available_dbs:
            print("Nenhum banco de dados de usuário encontrado ou acesso negado.")
            return

        print("\nBancos de dados disponíveis:")
        for i, db_name in enumerate(available_dbs):
            print(f"  [{i + 1}] {db_name}")

        database_name = ""
        while True:
            try:
                choice = int(input("\nEscolha o número do banco de dados para se conectar: ")) - 1
                if 0 <= choice < len(available_dbs):
                    database_name = available_dbs[choice]
                    print(f"Conectando ao banco de dados '{database_name}'...")
                    break
                else:
                    print("Escolha inválida. Por favor, digite um número da lista.")
            except ValueError:
                print("Entrada inválida. Por favor, digite um número.")
    
    except (psycopg2.Error, pymysql.Error) as e:
        print(f"Erro ao listar bancos de dados. Verifique suas credenciais. Erro: {e}")
        return
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao listar os bancos de dados: {e}")
        return
    
    # O resto do código continua como antes, agora com o database_name selecionado
    try:
        db = connect_db(db_engine, user, password, database_name)
        print("Conectado ao banco de dados com sucesso!")
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados '{database_name}': {e}")
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
                    df = pd.DataFrame(list(resultados), columns=colunas)
                    print(df.to_string())
                else: # Para queries que não retornam colunas (ex: DDL)
                    print("Comando executado com sucesso, sem resultados para exibir.")
            else:
                print("Nenhum resultado encontrado ou comando executado sem retorno.")
        
        except (psycopg2.Error, pymysql.Error) as e:
            print(f"Erro ao processar a consulta: {e}")
            db.rollback() # Importante para PostgreSQL em caso de erro na transação
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")

    if db:
        db.close()
    print("Programa encerrado.")

if __name__ == "__main__":
    main_loop()