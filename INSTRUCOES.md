# Instruções para Gerar as Imagens dos Resultados

Este guia explica como gerar as imagens dos resultados de análise de PRs.

## Opção 1: Usando API de LLM (Recomendado)

### Passo 1: Instalar dependências

```bash
pip install -r requirements.txt
```

### Passo 2: Configurar API Key (opcional)

Se você tiver acesso a OpenAI ou Anthropic:

```bash
export OPENAI_API_KEY="sua-chave-aqui"
# ou
export ANTHROPIC_API_KEY="sua-chave-aqui"
```

### Passo 3: Gerar resultados

```bash
python generate_results.py
```

Isso vai:
- Ler todos os prompts (v1, v2, v3)
- Ler todos os PRs (PR1 a PR6)
- Gerar respostas usando a API (ou mockadas se não tiver API key)
- Criar arquivos HTML formatados em `resultados/`

### Passo 4: Converter HTML em imagens

```bash
# Instalar Playwright
pip install playwright
playwright install chromium

# Gerar imagens
python generate_images.py
```

Isso vai converter todos os HTMLs em arquivos JPG.

---

## Opção 2: Manual (Sem API)

### Passo 1: Gerar HTMLs (com respostas mockadas)

```bash
python generate_results.py
```

Isso vai gerar HTMLs com respostas mockadas.

### Passo 2: Converter em imagens

Você tem várias opções:

#### A) Usar Playwright (automático)

```bash
pip install playwright
playwright install chromium
python generate_images.py
```

#### B) Usar ferramenta online

1. Acesse https://htmlcsstoimage.com/
2. Faça upload de cada arquivo HTML de `resultados/`
3. Baixe as imagens geradas

#### C) Screenshots manuais

1. Abra cada arquivo HTML no navegador
2. Tire screenshot (F12 → Device Toolbar → Screenshot)
3. Salve como JPG na pasta `resultados/` com o nome correto

---

## Opção 3: Usar ChatGPT/Claude diretamente

### Passo 1: Preparar prompts

Para cada combinação (v1-PR1, v1-PR2, etc.):

1. Abra o arquivo do prompt em `prompts/`
2. Abra o arquivo do PR em `documents/`
3. Substitua `{{descricao}}` e `{{conteudo}}` no prompt
4. Cole no ChatGPT/Claude
5. Capture screenshot do resultado
6. Salve como `v1-PR1.jpg`, etc.

### Script auxiliar para preparar prompts

```bash
python -c "
from pathlib import Path
import re

prompt = Path('prompts/v1-baseline.md').read_text()
pr = Path('documents/PR1-add-S3-bucket-to-logs.md').read_text()

desc_match = re.search(r'### Descrição do PR\n(.+?)\n###', pr, re.DOTALL)
content_match = re.search(r'```(?:text|terraform)?\n(.*?)```', pr, re.DOTALL)

desc = desc_match.group(1).strip() if desc_match else ''
cont = content_match.group(1).strip() if content_match else ''

final = prompt.replace('{{descricao}}', desc).replace('{{conteudo}}', cont)
print(final)
"
```

---

## Estrutura Final Esperada

Após executar, você deve ter:

```
resultados/
├── v1-PR1.html (ou .jpg)
├── v1-PR2.html (ou .jpg)
├── v1-PR3.html (ou .jpg)
├── v1-PR4.html (ou .jpg)
├── v1-PR5.html (ou .jpg)
├── v1-PR6.html (ou .jpg)
├── v2-PR1.html (ou .jpg)
├── v2-PR2.html (ou .jpg)
├── v2-PR3.html (ou .jpg)
├── v2-PR4.html (ou .jpg)
├── v2-PR5.html (ou .jpg)
├── v2-PR6.html (ou .jpg)
├── v3-PR1.html (ou .jpg)
├── v3-PR2.html (ou .jpg)
├── v3-PR3.html (ou .jpg)
├── v3-PR4.html (ou .jpg)
├── v3-PR5.html (ou .jpg)
└── v3-PR6.html (ou .jpg)
```

---

## Dicas

- Os HTMLs gerados são visualmente bonitos e prontos para screenshot
- Se usar API, as respostas serão mais realistas
- As respostas mockadas servem como exemplo do formato esperado
- Você pode editar `generate_results.py` para adicionar mais respostas mockadas realistas
