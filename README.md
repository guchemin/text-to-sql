# Conversor Text-to-SQL com Gemini (Interface Gráfica)

Este projeto converte perguntas em linguagem natural para consultas SQL utilizando o modelo **Gemini** da Google. Ele oferece tanto uma **interface gráfica com Tkinter** quanto uma interface de linha de comando para conectar-se a bancos PostgreSQL ou MySQL, gerar SQL com base no esquema do banco e visualizar os resultados diretamente.

![Text-to-SQL Generator](https://img.shields.io/badge/Text--to--SQL-Generator-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![Database](https://img.shields.io/badge/Database-PostgreSQL%20%7C%20MySQL-orange)
![Model](https://img.shields.io/badge/IA-Gemini%201.5%20Pro-yellow)
![GUI](https://img.shields.io/badge/Interface-Tkinter-lightgrey)

## 🚀 Características

- **Geração de SQL via Gemini**: Tradução precisa de linguagem natural para SQL
- **Interface gráfica intuitiva**: Desenvolvida com Tkinter
- **Suporte a múltiplos bancos**: Compatível com PostgreSQL e MySQL
- **Exibição de resultados formatados**: Visualização de dados via GUI
- **Prompt robusto + limpeza automática**: SQL puro, sem comentários ou markdown

## 📋 Pré-requisitos

- **Python 3.8+**
- Conta Google com chave da API Gemini (colocada no `.env`)
- Banco de dados PostgreSQL ou MySQL rodando localmente

## 🔧 Instalação

```bash
git clone https://github.com/guchemin/text-to-sql.git
cd text-to-sql
pip install -r requirements.txt
```

Crie o arquivo `.env` na raiz:

```
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

## 🖥️ Como usar

### Interface Gráfica (Tkinter)

```bash
python gui.py
```

### Linha de Comando (modo clássico)

```bash
python script.py
```

## 📊 Exemplos de Pergunta

```
"Quais alunos estão matriculados no curso de Engenharia?"
"Mostre os produtos com estoque abaixo de 10 unidades"
"Quantos pedidos foram feitos em março?"
"Liste os professores por ordem alfabética"
```

## 🛠️ Estrutura do Projeto

```
text-to-sql/
├── script.py           # CLI interativa
├── gui.py              # Interface gráfica (Tkinter)
├── .env                # Chave da API Gemini
├── README.md           # Documentação
└── .gitignore
```

## 🐛 Dicas de Solução de Problemas

- **Erro: GOOGLE_API_KEY não definida**
  - Verifique se criou o `.env` corretamente

- **Erro de conexão com banco:**
  - Confirme que o banco está rodando em `localhost`
  - Verifique credenciais, nome do banco e porta

- **SQL inválido gerado:**
  - Use perguntas mais específicas
  - Verifique se a estrutura do banco está correta

## 🔗 Fontes e Links

- [Gemini API](https://ai.google.dev/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [MySQL Docs](https://dev.mysql.com/doc/)
- [Tkinter Docs](https://docs.python.org/3/library/tkinter.html)