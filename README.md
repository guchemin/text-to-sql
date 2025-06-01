# Conversor Text-to-SQL com Ollama e Qwen

Este projeto converte perguntas em linguagem natural para consultas SQL usando o modelo Qwen da Ollama. Disponível em duas interfaces: linha de comando e interface gráfica moderna com CustomTkinter.

![Text-to-SQL Generator](https://img.shields.io/badge/Text--to--SQL-Generator-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![Database](https://img.shields.io/badge/Database-PostgreSQL%20%7C%20MySQL-orange)

---

## 🚀 Características

- **Interface Gráfica Moderna**: Interface intuitiva com design responsivo usando CustomTkinter
- **Suporte Multi-Banco**: Compatível com PostgreSQL e MySQL
- **IA Integrada**: Utiliza modelo Qwen via Ollama para geração de SQL
- **Execução Automática**: Gera e executa automaticamente as consultas SQL
- **Visualização de Resultados**: Exibe resultados em tabelas organizadas
- **Rolagem Contextual**: Sistema de rolagem inteligente para melhor experiência
- **Tema Adaptativo**: Suporte a temas claro/escuro

---

## 📋 Pré-requisitos

### Software Necessário

1. **Python 3.8+**
2. **Ollama** instalado e rodando localmente
3. **Banco de dados** (PostgreSQL ou MySQL) configurado
4. **Modelo Qwen** baixado via Ollama

### Banco de Dados

- **PostgreSQL 12+** ou **MySQL 8.0+**
- Banco de dados configurado e acessível via `localhost`
- Usuário com permissões de leitura nas tabelas

---

## 🔧 Instalação

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd text-to-sql
```

### 2. Instale as dependências Python

```bash
pip install ollama customtkinter pandas psycopg2-binary pymysql
```

**Ou use o requirements.txt:**

```bash
pip install -r requirements.txt
```

### 3. Configure o Ollama

```bash
# Instale o Ollama (se ainda não tiver)
curl -fsSL https://ollama.ai/install.sh | sh

# Baixe o modelo Qwen
ollama pull qwen3:0.6b

# Inicie o servidor Ollama
ollama serve
```

### 4. Configure seu banco de dados

Certifique-se de que seu banco PostgreSQL ou MySQL está rodando e acessível em `localhost`.

---

## 🖥️ Como usar

### Interface Gráfica (Recomendado)

1. **Inicie o servidor Ollama:**
```bash
ollama serve
```

2. **Execute a interface gráfica:**
```bash
python gui.py
```

3. **Configure a conexão:**
   - Selecione o motor do banco (PostgreSQL/MySQL)
   - Digite usuário, senha e nome do banco
   - Clique em "Conectar e Carregar Schema"

4. **Faça perguntas:**
   - Digite sua pergunta em linguagem natural
   - Clique em "Gerar SQL"
   - Veja o SQL gerado e os resultados automaticamente

### Interface de Linha de Comando

```bash
python script.py
```

Siga as instruções no terminal para conectar ao banco e fazer perguntas.

---

## 📊 Exemplos de Uso

### Perguntas Exemplo

```
"Quais funcionários trabalham no departamento de vendas?"
"Mostre todos os produtos com preço maior que 100"
"Quantos pedidos foram feitos este mês?"
"Liste os clientes por ordem alfabética"
"Qual o funcionário com maior salário?"
```

### Saída Esperada

**SQL Gerada:**
```sql
SELECT e.nome, e.sobrenome 
FROM funcionarios e 
JOIN departamentos d ON e.departamento_id = d.id 
WHERE d.nome = 'vendas';
```

**Resultados:**
```
nome     | sobrenome
---------|----------
João     | Silva
Maria    | Santos
```

---

## 🎨 Interface Gráfica - Recursos

### Design Moderno
- **Tema responsivo** com suporte a claro/escuro
- **Layout centralizado** e organizado
- **Tipografia aprimorada** para melhor legibilidade
- **Cores personalizadas** para status e feedback

### Experiência do Usuário
- **Rolagem contextual**: Rola o conteúdo certo baseado na posição do cursor
- **Feedback visual**: Indicadores de status em tempo real
- **Validação de entrada**: Verificação automática de campos obrigatórios
- **Redimensionamento inteligente**: Interface se adapta ao tamanho da tela

### Funcionalidades Avançadas
- **Schema automático**: Carregamento e exibição do esquema do banco
- **Execução automática**: Gera e executa SQL em uma única ação
- **Tabela de resultados**: Exibição organizada com cabeçalhos alinhados
- **Tratamento de erros**: Mensagens claras para debugging

---

## 🔧 Configurações

### Modelos Ollama Alternativos

Para usar um modelo diferente, edite o arquivo `script.py`:

```python
# Linha 75 - altere o modelo
resposta = client.chat(
    model='qwen3:0.6b',  # Altere aqui
    messages=[{'role': 'user', 'content': prompt}]
)
```

### Conexão com Banco Remoto

Para conectar a um banco remoto, modifique as funções de conexão em `script.py`:

```python
# Para PostgreSQL
db = psycopg2.connect(
    host='seu-host-remoto',  # Altere aqui
    database=database_name,
    user=user,
    password=password,
    port=5432  # Adicione se necessário
)
```

---

## 🛠️ Estrutura do Projeto

```
text-to-sql/
├── gui.py              # Interface gráfica moderna
├── script.py           # Lógica principal e interface CLI
├── README.md           # Documentação
├── requirements.txt    # Dependências Python
└── .gitignore         # Arquivos ignorados pelo Git
```

---

## 🐛 Troubleshooting

### Problemas Comuns

**Erro de conexão com Ollama:**
```bash
# Verifique se o Ollama está rodando
ollama list
ollama serve
```

**Erro de conexão com banco:**
- Verifique se o banco está rodando
- Confirme usuário/senha/nome do banco
- Teste conexão manual

**Dependências não encontradas:**
```bash
pip install --upgrade ollama customtkinter psycopg2-binary pymysql pandas
```

**Interface não responsiva:**
- Verifique se está usando Python 3.8+
- Tente redimensionar a janela
- Reinicie a aplicação

---

## 📝 Notas Técnicas

### Sobre o Modelo
- **Modelo usado**: `qwen3:0.6b` (otimizado para velocidade)
- **Prompt otimizado**: Força respostas SQL diretas sem explicações
- **Limpeza automática**: Remove tags `<think>` automaticamente

### Sobre a Interface
- **Framework**: CustomTkinter para aparência moderna
- **Compatibilidade**: Linux, Windows, macOS
- **Resolução**: Responsivo a partir de 1000x750px

### Sobre Bancos Suportados
- **PostgreSQL**: Versão 12+ recomendada
- **MySQL**: Versão 8.0+ recomendada
- **Esquemas**: Detecção automática via `information_schema`

---

## 🔗 Links Úteis

- [Ollama Documentation](https://ollama.ai/docs)
- [CustomTkinter Documentation](https://customtkinter.tomschimansky.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [MySQL Documentation](https://dev.mysql.com/doc/)