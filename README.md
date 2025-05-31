# Conversor Text-to-SQL com Ollama e Qwen

Este projeto converte perguntas em linguagem natural para consultas SQL usando o modelo Qwen da Ollama.

---

## Pré-requisitos

- Ollama instalado e rodando localmente (`ollama serve`)
- Modelo Qwen baixado (exemplo: `qwen3:0.6b`)
- Python 3.8+
- Biblioteca Ollama para Python instalada:

```bash
pip install ollama
```

---

## Como usar

1. Inicie o servidor Ollama:

```bash
ollama serve
```

2. Execute o script:

```bash
python3 script.py
```

3. Digite sua pergunta em linguagem natural, por exemplo:

```
Quais funcionários trabalham no departamento de vendas?
```

4. O script irá retornar a consulta SQL gerada.

---

## Sobre o código

- O prompt força respostas diretas, sem explicações ou tags `<think>`.
- O script remove automaticamente qualquer trecho `<think>` da resposta.
- Modelo usado: `qwen3:0.6b` (pode ser alterado conforme disponível).