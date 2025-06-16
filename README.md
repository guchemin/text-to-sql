# Text-to-SQL Generator com Gemini

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Database](https://img.shields.io/badge/Database-PostgreSQL%20%7C%20MySQL-orange.svg)](https://postgresql.org/)
[![AI](https://img.shields.io/badge/IA-Gemini%201.5%20Pro-yellow.svg)](https://ai.google.dev/)
[![GUI](https://img.shields.io/badge/Interface-CustomTkinter-green.svg)](https://github.com/TomSchimansky/CustomTkinter)
[![License](https://img.shields.io/badge/License-MIT-red.svg)](LICENSE)

## 📖 Sobre o Projeto

Este projeto converte **perguntas em linguagem natural** para **consultas SQL** utilizando o modelo **Gemini 1.5 Pro** da Google. Oferece uma interface gráfica moderna e intuitiva construída com CustomTkinter, além de funcionalidades avançadas como exportação de resultados e visualização de dados.

### ✨ Funcionalidades Principais

- 🤖 **IA Avançada**: Utiliza Gemini 1.5 Pro para tradução precisa de linguagem natural para SQL
- 🎨 **Interface Moderna**: GUI responsiva e elegante com tema escuro
- 🗄️ **Multi-Database**: Suporte completo para PostgreSQL e MySQL
- 📊 **Visualização Inteligente**: Tabela de resultados com numeração automática
- 📁 **Exportação CSV**: Salve resultados diretamente em arquivos CSV
- 🔄 **Rolagem Contextual**: Navegação intuitiva com mouse wheel
- 📱 **Design Responsivo**: Interface adaptável a diferentes tamanhos de tela
- 🔧 **CLI Alternativa**: Modo linha de comando para uso avançado

## 🖼️ Interface

A aplicação possui uma interface moderna dividida em seções organizadas:

1. **Conexão com Banco**: Configuração de credenciais e tipos de banco
2. **Schema**: Visualização automática da estrutura do banco
3. **Consulta Natural**: Campo para inserir perguntas em linguagem natural
4. **SQL Gerada**: Exibição da consulta SQL criada pela IA
5. **Resultados**: Tabela com dados e opção de exportação CSV

## 🚀 Instalação Rápida

### Pré-requisitos

- **Python 3.8+**
- **PostgreSQL** ou **MySQL** instalado e rodando
- **Chave API do Google Gemini** ([Obter aqui](https://ai.google.dev/))

### Passos de Instalação

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/text-to-sql.git
cd text-to-sql
```

2. **Crie um ambiente virtual** (recomendado)
```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente**
   
   Crie um arquivo `.env` na raiz do projeto:
```env
GOOGLE_API_KEY=sua_chave_da_api_gemini_aqui
```

5. **Execute a aplicação**
```bash
# Interface Gráfica (Recomendado)
python gui.py

# Ou modo linha de comando
python script.py
```

## 🎯 Como Usar

### Interface Gráfica

1. **Conecte ao Banco**:
   - Escolha o motor (PostgreSQL/MySQL)
   - Insira usuário, senha e nome do banco
   - Clique em "Conectar e Carregar Schema"

2. **Faça sua Pergunta**:
   - Digite uma pergunta em linguagem natural
   - Clique em "Gerar SQL"
   - Visualize a SQL gerada e os resultados

3. **Exporte Resultados** (opcional):
   - Clique em "Salvar CSV" para exportar os dados
   - Escolha o local e nome do arquivo

### Exemplos de Perguntas

| Categoria | Exemplo |
|-----------|---------|
| **Listagem** | "Mostre todos os alunos" |
| **Filtros** | "Quais produtos custam mais de R$ 100?" |
| **Agregações** | "Quantos pedidos foram feitos este mês?" |
| **Joins** | "Liste os alunos e seus cursos" |
| **Ordenação** | "Professores ordenados por salário" |

## 📁 Estrutura do Projeto

```
text-to-sql/
├── 📄 gui.py              # Interface gráfica principal
├── 📄 script.py           # Lógica de negócio e CLI
├── 📄 requirements.txt    # Dependências do projeto
├── 🔧 .env                # Variáveis de ambiente (criar)
├── 📋 .env.template       # Template para variáveis
├── 📖 README.md           # Documentação
└── 📁 venv/               # Ambiente virtual (criado)
```

## 🔧 Dependências

### Principais Bibliotecas

- **customtkinter**: Interface gráfica moderna
- **google-generativeai**: API do Gemini
- **psycopg2-binary**: Driver PostgreSQL
- **PyMySQL**: Driver MySQL
- **pandas**: Manipulação de dados
- **python-dotenv**: Gerenciamento de variáveis

### Instalação Manual

Se preferir instalar manualmente:

```bash
pip install customtkinter==5.2.2
pip install google-generativeai==0.8.5
pip install psycopg2-binary==2.9.10
pip install PyMySQL==1.1.1
pip install pandas==2.3.0
pip install python-dotenv==1.1.0
pip install cryptography==45.0.4
```

## 🛠️ Solução de Problemas

### Problemas Comuns

#### ❌ "GOOGLE_API_KEY não definida"
```bash
# Verifique se o arquivo .env existe e contém:
GOOGLE_API_KEY=sua_chave_aqui
```

#### ❌ Erro de conexão com banco
```bash
# Verifique se o banco está rodando:
# PostgreSQL
sudo systemctl status postgresql

# MySQL
sudo systemctl status mysql
```

#### ❌ Módulo 'customtkinter' não encontrado
```bash
# Instale novamente as dependências:
pip install --upgrade -r requirements.txt
```

#### ❌ Erro de encoding no Windows
```bash
# Execute com encoding UTF-8:
python -X utf8 gui.py
```

### Problemas de Performance

- **SQL lenta**: Use perguntas mais específicas
- **Interface travando**: Verifique conexão com internet (API Gemini)
- **Erro de memória**: Limite resultados com "LIMIT" nas perguntas

## 🔗 APIs e Tecnologias

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| [Python](https://python.org) | 3.8+ | Linguagem principal |
| [Gemini API](https://ai.google.dev/) | 1.5 Pro | Geração de SQL |
| [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) | 5.2.2 | Interface gráfica |
| [PostgreSQL](https://postgresql.org) | Any | Banco de dados |
| [MySQL](https://mysql.com) | Any | Banco de dados |

## 📝 Exemplos Avançados

### Consultas Complexas
```sql
-- Pergunta: "Mostre os 5 produtos mais vendidos este ano"
-- SQL Gerada:
SELECT p.nome, SUM(i.quantidade) as total_vendido
FROM produtos p
JOIN itens_pedido i ON p.id = i.produto_id
JOIN pedidos pe ON i.pedido_id = pe.id
WHERE YEAR(pe.data_pedido) = YEAR(CURRENT_DATE)
GROUP BY p.id, p.nome
ORDER BY total_vendido DESC
LIMIT 5;
```

### Exportação Personalizada
- Resultados incluem coluna de índice automática
- Formato CSV compatível com Excel
- Preserva acentos e caracteres especiais

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

