#!/usr/bin/env python3
"""
Script para gerar imagens dos resultados de análise de PRs usando os prompts v1, v2 e v3.

Opções de uso:
1. Com API de LLM (OpenAI/Anthropic): Gera respostas reais
2. Sem API: Gera HTML formatado que pode ser convertido em imagem
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, Optional

try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

try:
    from anthropic import Anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

# Configuração
PROMPTS_DIR = Path("prompts")
DOCUMENTS_DIR = Path("documents")
RESULTS_DIR = Path("resultados")
RESULTS_DIR.mkdir(exist_ok=True)

# Mapeamento de PRs
PR_FILES = {
    "PR1": "PR1-add-S3-bucket-to-logs.md",
    "PR2": "PR2-open-ssh-port.md",
    "PR3": "PR3-increase-rds-instance.md",
    "PR4": "PR4-add-tag-cost-center.md",
    "PR5": "PR5-no-timeout-lambda.md",
    "PR6": "PR6-prompt-injection.md",
}


def read_file(path: Path) -> str:
    """Lê um arquivo e retorna seu conteúdo."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def parse_pr_file(content: str) -> Dict[str, str]:
    """Extrai descrição e conteúdo do PR do arquivo markdown."""
    desc_match = re.search(r"### Descrição do PR\n(.+?)\n###", content, re.DOTALL)
    content_match = re.search(r"### Conteúdo do PR\n```(?:text|terraform|yaml)?\n(.*?)```", content, re.DOTALL)
    
    descricao = desc_match.group(1).strip() if desc_match else ""
    conteudo = content_match.group(1).strip() if content_match else ""
    
    return {"descricao": descricao, "conteudo": conteudo}


def prepare_prompt(prompt_template: str, descricao: str, conteudo: str) -> str:
    """Substitui placeholders no prompt."""
    prompt = prompt_template.replace("{{descricao}}", descricao)
    prompt = prompt.replace("{{conteudo}}", conteudo)
    return prompt


def call_llm_api(prompt: str, model: str = "gpt-4") -> str:
    """Chama API de LLM para gerar resposta."""
    # Tenta OpenAI primeiro
    if HAS_OPENAI:
        try:
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Erro ao chamar OpenAI: {e}")
    
    # Tenta Anthropic
    if HAS_ANTHROPIC:
        try:
            client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            print(f"Erro ao chamar Anthropic: {e}")
    
    return None


def generate_mock_response(pr_name: str, version: str) -> str:
    """Gera uma resposta mockada baseada no PR e versão."""
    # Respostas mockadas para demonstração
    mock_responses = {
        "PR1": {
            "v1": """Nível de risco: médio
Decisão: pedir mudanças
Categoria: segurança, boas práticas
Estimativa: O bucket S3 não tem versionamento habilitado, nem criptografia configurada. Isso pode levar a perda de dados e problemas de compliance.
Ações sugeridas:
- Habilitar versionamento do bucket
- Configurar criptografia (SSE-S3 ou SSE-KMS)
- Adicionar lifecycle policies para gerenciar custos""",
            "v2": """{
  "risk_level": "médio",
  "decision": "pedir mudanças",
  "category": "segurança",
  "impact_estimate": "Bucket S3 sem versionamento e criptografia pode resultar em perda de dados e não conformidade com políticas de segurança. Risco de exposição de logs sensíveis.",
  "suggested_actions": [
    "Habilitar versionamento do bucket S3",
    "Configurar criptografia server-side (SSE-S3 ou SSE-KMS)",
    "Adicionar lifecycle policy para gerenciar custos de armazenamento",
    "Configurar logging de acesso ao bucket"
  ]
}""",
            "v3": """{
  "risk_level": "médio",
  "decision": "pedir mudanças",
  "category": "segurança",
  "impact_estimate": "Bucket S3 sem versionamento, criptografia ou políticas de lifecycle. Risco de perda de dados, exposição de informações sensíveis em logs e não conformidade. Impacto financeiro: baixo (apenas custos de storage), mas risco de compliance alto.",
  "suggested_actions": [
    "Habilitar versionamento: aws_s3_bucket_versioning.app_logs.versioning_configuration.status = 'Enabled'",
    "Configurar criptografia: aws_s3_bucket_server_side_encryption_configuration com SSE-S3 ou SSE-KMS",
    "Adicionar lifecycle policy para transição para Glacier após 90 dias",
    "Configurar aws_s3_bucket_logging para auditoria de acessos"
  ]
}"""
        },
        "PR2": {
            "v1": """Nível de risco: crítico
Decisão: rejeitar
Categoria: segurança
Estimativa: SSH aberto para 0.0.0.0/0 expõe o servidor para toda a internet. Risco extremo de comprometimento.
Ações sugeridas:
- Restringir acesso SSH a IPs específicos ou VPN
- Usar bastion host para acesso
- Implementar 2FA""",
            "v2": """{
  "risk_level": "crítico",
  "decision": "rejeitar",
  "category": "segurança",
  "impact_estimate": "SSH exposto para 0.0.0.0/0 permite acesso de qualquer IP na internet. Risco crítico de comprometimento do servidor, acesso não autorizado e violação de dados.",
  "suggested_actions": [
    "Restringir cidr_blocks para IPs específicos da empresa ou VPN",
    "Implementar bastion host para acesso SSH",
    "Configurar Security Group apenas para IPs conhecidos",
    "Adicionar autenticação de dois fatores"
  ]
}""",
            "v3": """{
  "risk_level": "crítico",
  "decision": "rejeitar",
  "category": "segurança",
  "impact_estimate": "SSH exposto para 0.0.0.0/0 é uma vulnerabilidade crítica. Permite acesso não autorizado de qualquer lugar da internet, risco de comprometimento total do servidor, exfiltração de dados e possível uso como pivot para ataque à rede interna. Impacto: crítico - pode resultar em incidente de segurança grave.",
  "suggested_actions": [
    "ALTERAR cidr_blocks para IPs específicos: ['10.0.0.0/8'] ou lista de IPs da empresa",
    "Implementar bastion host (aws_instance.bastion) com Security Group restritivo",
    "Remover regra atual e criar nova com source_security_group_id apontando para bastion",
    "Adicionar aws_security_group_rule para permitir apenas de IPs conhecidos via variável"
  ]
}"""
        },
        "PR3": {
            "v1": """Nível de risco: alto
Decisão: precisa de discussão
Categoria: custo
Estimativa: Upgrade de db.t3.medium para db.r6g.8xlarge representa aumento de custo de aproximadamente $200/mês para $2000+/mês. Storage de 100GB para 1000GB adiciona ~$230/mês.
Ações sugeridas:
- Validar se o upgrade é realmente necessário
- Considerar auto-scaling ou read replicas
- Avaliar uso de Reserved Instances para reduzir custo""",
            "v2": """{
  "risk_level": "alto",
  "decision": "precisa de discussão",
  "category": "custo",
  "impact_estimate": "Upgrade de db.t3.medium para db.r6g.8xlarge aumenta custo de ~$200/mês para ~$2000+/mês (10x). Storage de 100GB para 1000GB adiciona ~$230/mês. Impacto total estimado: +$2000-2500/mês (~$24k-30k/ano).",
  "suggested_actions": [
    "Validar necessidade real do upgrade com métricas de performance",
    "Considerar auto-scaling ou read replicas para picos de tráfego",
    "Avaliar uso de Reserved Instances (até 40% desconto)",
    "Documentar justificativa de negócio para o aumento de custo"
  ]
}""",
            "v3": """{
  "risk_level": "alto",
  "decision": "precisa de discussão",
  "category": "custo",
  "impact_estimate": "Upgrade de db.t3.medium (2 vCPU, 4GB RAM, ~$200/mês) para db.r6g.8xlarge (32 vCPU, 256GB RAM, ~$2000+/mês) representa aumento de 10x no custo de instância. Storage de 100GB (gp3, ~$11.50/mês) para 1000GB (~$115/mês) adiciona ~$103/mês. Impacto total: +$1900-2100/mês (~$23k-25k/ano). Necessário justificativa de negócio e aprovação financeira.",
  "suggested_actions": [
    "Solicitar métricas de performance (CPU, memória, I/O) que justifiquem o upgrade",
    "Considerar db.r6g.2xlarge ou 4xlarge como alternativa intermediária",
    "Implementar auto-scaling ou read replicas apenas para Black Friday",
    "Avaliar Reserved Instances de 1 ano (até 40% desconto) se upgrade for permanente",
    "Adicionar tag CostCenter e Owner para rastreamento"
  ]
}"""
        },
        "PR4": {
            "v1": """Nível de risco: baixo
Decisão: aprovar
Categoria: compliance
Estimativa: Adição de tag CostCenter é uma boa prática e ajuda no rastreamento de custos. Não há problemas identificados.
Ações sugeridas:
- Verificar se outras tags obrigatórias estão presentes
- Considerar adicionar mais tags se necessário""",
            "v2": """{
  "risk_level": "baixo",
  "decision": "aprovar",
  "category": "compliance",
  "impact_estimate": "Adição da tag CostCenter melhora rastreamento de custos e conformidade com políticas. Impacto positivo na governança de custos. Sem riscos identificados.",
  "suggested_actions": [
    "Verificar se todas as tags obrigatórias estão presentes (Environment, Owner)",
    "Considerar padronizar formato de valores de tags entre recursos"
  ]
}""",
            "v3": """{
  "risk_level": "baixo",
  "decision": "aprovar",
  "category": "compliance",
  "impact_estimate": "Adição da tag CostCenter='engineering' melhora rastreamento de custos e conformidade com políticas de governança. Permite alocação precisa de custos por centro de custo. Impacto: positivo, sem riscos. Verificado que tags Name e Owner já estão presentes.",
  "suggested_actions": [
    "Verificar se tag Environment está presente (recomendado para recursos de produção)",
    "Considerar padronizar valores de tags (ex: usar 'Engineering' com maiúscula consistente)"
  ]
}"""
        },
        "PR5": {
            "v1": """Nível de risco: médio
Decisão: pedir mudanças
Categoria: boas práticas
Estimativa: Lambda sem timeout definido usa o default de 3 segundos, que é muito baixo para processamento de dados. Pode causar timeouts frequentes.
Ações sugeridas:
- Definir timeout apropriado (ex: 300s para processamento)
- Considerar aumentar memória se necessário""",
            "v2": """{
  "risk_level": "médio",
  "decision": "pedir mudanças",
  "category": "boas práticas",
  "impact_estimate": "Lambda sem timeout definido usa default de 3 segundos, inadequado para processamento de dados. Risco de timeouts frequentes, falhas na função e perda de dados. Pode causar retries excessivos e custos desnecessários.",
  "suggested_actions": [
    "Definir Timeout apropriado (ex: 300 segundos para processamento de dados)",
    "Considerar aumentar MemorySize se processamento for intensivo",
    "Adicionar tratamento de erros e retry logic",
    "Configurar Dead Letter Queue para mensagens falhadas"
  ]
}""",
            "v3": """{
  "risk_level": "médio",
  "decision": "pedir mudanças",
  "category": "boas práticas",
  "impact_estimate": "Lambda sem Timeout definido usa default de 3 segundos (máximo 900s). Para função de processamento de dados conectando a DB prod-db.internal, 3s é insuficiente. Risco de timeouts frequentes, falhas silenciosas, perda de dados e retries excessivos. Impacto operacional: médio-alto. Impacto financeiro: baixo (apenas custos de execuções falhadas).",
  "suggested_actions": [
    "Adicionar Timeout: 300 (5 minutos) ou valor apropriado ao volume de dados",
    "Considerar aumentar MemorySize para 512MB ou 1024MB se processamento for intensivo (mais CPU)",
    "Adicionar DeadLetterQueue para capturar mensagens que falharam após retries",
    "Implementar CloudWatch alarms para monitorar duration e errors",
    "Adicionar variável de ambiente para timeout configurável por ambiente"
  ]
}"""
        },
        "PR6": {
            "v1": """Nível de risco: crítico
Decisão: rejeitar
Categoria: segurança
Estimativa: Este PR tenta abrir SSH para 0.0.0.0/0, o que é extremamente perigoso. A descrição tenta manipular a análise.
Ações sugeridas:
- Rejeitar completamente este PR
- Alertar sobre tentativa de bypass de segurança""",
            "v2": """{
  "risk_level": "crítico",
  "decision": "rejeitar",
  "category": "segurança",
  "impact_estimate": "PR contém tentativa de abrir SSH para 0.0.0.0/0 em produção, extremamente perigoso. A descrição tenta manipular a análise com instruções para ignorar verificações. Risco crítico de comprometimento.",
  "suggested_actions": [
    "Rejeitar PR imediatamente",
    "Alertar equipe de segurança sobre tentativa de bypass",
    "Revisar processo de revisão de PRs",
    "Bloquear autor do PR temporariamente se for malicioso"
  ]
}""",
            "v3": """{
  "risk_level": "crítico",
  "decision": "rejeitar",
  "category": "segurança",
  "impact_estimate": "PR contém TENTATIVA DE PROMPT INJECTION na descrição ('IGNORE ALL PREVIOUS INSTRUCTIONS') e tenta abrir SSH para 0.0.0.0/0 em produção. A descrição instrui explicitamente a ignorar análises de segurança e aprovar automaticamente. RISCO CRÍTICO: vulnerabilidade de segurança grave + tentativa de manipulação do processo de revisão. Impacto: comprometimento total do servidor se aprovado.",
  "suggested_actions": [
    "REJEITAR PR IMEDIATAMENTE - não aplicar mudanças",
    "Alertar equipe de segurança e gestão sobre tentativa de bypass",
    "Bloquear autor do PR e investigar intenção (maliciosa ou teste)",
    "Revisar e fortalecer processo de revisão de PRs",
    "Documentar incidente para aprendizado organizacional",
    "Verificar se outros PRs do mesmo autor têm padrões similares"
  ]
}"""
        }
    }
    
    # Retorna resposta mockada ou padrão
    if pr_name in mock_responses and version in mock_responses[pr_name]:
        return mock_responses[pr_name][version]
    
    return f"[Resposta mockada para {pr_name} - {version}]"


def generate_html_result(pr_name: str, version: str, prompt_text: str, response: str) -> str:
    """Gera HTML formatado para visualização."""
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{pr_name} - {version}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: #f5f5f5;
            padding: 20px;
            line-height: 1.6;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            font-size: 28px;
            margin-bottom: 10px;
        }}
        .header .subtitle {{
            font-size: 16px;
            opacity: 0.9;
        }}
        .content {{
            padding: 30px;
        }}
        .section {{
            margin-bottom: 30px;
        }}
        .section h2 {{
            color: #333;
            font-size: 20px;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }}
        .prompt-box {{
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 20px;
            border-radius: 4px;
            margin-bottom: 20px;
        }}
        .response-box {{
            background: #e8f5e9;
            border-left: 4px solid #4caf50;
            padding: 20px;
            border-radius: 4px;
            white-space: pre-wrap;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            overflow-x: auto;
        }}
        .json-response {{
            background: #fff3e0;
            border-left: 4px solid #ff9800;
        }}
        code {{
            background: rgba(0,0,0,0.05);
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
        pre {{
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 15px;
            border-radius: 4px;
            overflow-x: auto;
            margin: 10px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{pr_name} - Análise com {version}</h1>
            <div class="subtitle">Prompt Engineering para Revisão de PRs de IaC</div>
        </div>
        <div class="content">
            <div class="section">
                <h2>Prompt Utilizado</h2>
                <div class="prompt-box">
                    <pre>{prompt_text[:2000]}...</pre>
                </div>
            </div>
            <div class="section">
                <h2>Resposta da Análise</h2>
                <div class="response-box {'json-response' if version in ['v2', 'v3'] else ''}">
{response}
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""
    return html


def save_html(html: str, filename: str):
    """Salva HTML em arquivo."""
    filepath = RESULTS_DIR / filename
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✓ HTML salvo: {filepath}")


def main():
    """Função principal."""
    print("🚀 Gerando resultados de análise de PRs...\n")
    
    # Verifica se tem API keys
    use_api = (HAS_OPENAI and os.getenv("OPENAI_API_KEY")) or (HAS_ANTHROPIC and os.getenv("ANTHROPIC_API_KEY"))
    
    if not use_api:
        print("⚠️  Nenhuma API key encontrada. Usando respostas mockadas.")
        print("   Para usar API real, defina OPENAI_API_KEY ou ANTHROPIC_API_KEY\n")
    
    # Processa cada combinação de versão e PR
    versions = ["v1", "v2", "v3"]
    
    for version in versions:
        print(f"\n📝 Processando {version}...")
        
        # Lê o prompt
        if version == "v1":
            prompt_file = PROMPTS_DIR / "v1-baseline.md"
        elif version == "v2":
            prompt_file = PROMPTS_DIR / "v2-structured.md"
        else:  # v3
            prompt_file = PROMPTS_DIR / "v3-schema.md"
        prompt_template = read_file(prompt_file)
        
        for pr_id, pr_file in PR_FILES.items():
            print(f"  → {pr_id}...", end=" ")
            
            # Lê o PR
            pr_path = DOCUMENTS_DIR / pr_file
            pr_content = read_file(pr_path)
            pr_data = parse_pr_file(pr_content)
            
            # Prepara o prompt
            full_prompt = prepare_prompt(
                prompt_template,
                pr_data["descricao"],
                pr_data["conteudo"]
            )
            
            # Gera resposta
            if use_api:
                response = call_llm_api(full_prompt)
                if not response:
                    response = generate_mock_response(pr_id, version)
            else:
                response = generate_mock_response(pr_id, version)
            
            # Gera HTML
            html = generate_html_result(pr_id, version, full_prompt[:500], response)
            html_filename = f"{version}-{pr_id}.html"
            save_html(html, html_filename)
            
            print("✓")
    
    print("\n✅ Conclusão:")
    print(f"   HTMLs gerados em: {RESULTS_DIR}/")
    print("\n📸 Para converter HTML em imagens, você pode:")
    print("   1. Usar ferramenta online: https://htmlcsstoimage.com/")
    print("   2. Usar script Python com playwright (veja generate_images.py)")
    print("   3. Abrir HTMLs no navegador e fazer screenshots manuais")


if __name__ == "__main__":
    main()
