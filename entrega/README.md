# Análise Automática de Pull Requests - Prompt Engineering

**Nome do Aluno**: Washington Neris Santana

## Objetivo

Este projeto demonstra a evolução de prompts para análise automática de Pull Requests de Infrastructure as Code (IaC), com foco em segurança, custo, compliance e boas práticas. Cada versão representa uma melhoria incremental em relação à anterior.

## Estrutura do Projeto

```
├── prompts/
│   ├── v1-baseline.md          # Versão básica do prompt
│   ├── v2-structured.md        # Versão estruturada com formato JSON
│   └── v3-schema.md            # Versão completa com proteção contra prompt injection
├── resultados/
│   └── [prints dos resultados de cada versão para cada PR]
└── README.md
```

## Raciocínio por Versão

### Versão 1 (v1-baseline.md) - Baseline

**Abordagem**: Prompt simples e direto, sem estruturação rígida.

**Características**:
- Instruções básicas sobre o papel do revisor
- Lista simples dos campos de resposta esperados
- Sem formatação específica de saída
- Sem proteção contra manipulação

**Limitações identificadas**:
- Respostas podem ser inconsistentes em formato
- Não há validação de estrutura de saída
- Vulnerável a prompt injection
- Falta de critérios específicos de análise
- Pode gerar respostas verbosas ou incompletas

**Uso**: Serve como ponto de partida para demonstrar a necessidade de melhorias.

---

### Versão 2 (v2-structured.md) - Structured

**Abordagem**: Adiciona estruturação e critérios específicos de análise.

**Melhorias em relação à v1**:
1. **Critérios explícitos de análise**: Define categorias claras (Segurança, Custo, Compliance, Boas Práticas) com sub-itens específicos
2. **Formato de saída estruturado**: Exige resposta em JSON com campos específicos, garantindo consistência
3. **Contexto profissional**: Estabelece o papel de "engenheiro sênior" para maior rigor
4. **Instruções mais detalhadas**: Cada categoria tem critérios específicos a verificar

**Características**:
- Formato JSON obrigatório para resposta
- Critérios de análise organizados por categoria
- Melhor orientação sobre o que verificar
- Mais consistência nas respostas

**Limitações ainda presentes**:
- Ainda vulnerável a prompt injection (PR6 pode manipular)
- Não há validação de schema JSON
- Falta de checklist explícito para garantir todas as verificações
- Não há proteção explícita contra instruções maliciosas no PR

**Uso**: Demonstra a importância de estruturação e critérios claros.

---

### Versão 3 (v3-schema.md) - Schema with Prompt Injection Protection

**Abordagem**: Versão completa com proteção robusta e schema validado.

**Melhorias em relação à v2**:
1. **Proteção contra Prompt Injection**:
   - Seção explícita alertando sobre tentativas de manipulação
   - Instrução clara para ignorar comandos na descrição do PR
   - Regra crítica destacada no início do prompt
   - Processo de análise que reforça a execução de todas as verificações

2. **Checklist explícito**: Cada categoria tem uma lista de verificação (checkboxes) que força a análise completa

3. **Schema JSON detalhado**: 
   - Define valores permitidos para cada campo
   - Explica o significado de cada opção
   - Garante respostas válidas e consistentes

4. **Processo de análise passo a passo**: Define um fluxo claro de 7 etapas que o modelo deve seguir

5. **Instruções mais específicas**:
   - Detalha o que constitui cada nível de risco
   - Explica quando usar cada tipo de decisão
   - Solicita ações "específicas e acionáveis" em vez de genéricas

6. **Reforço de segurança**: Múltiplas camadas de proteção contra manipulação:
   - Alerta inicial sobre prompt injection
   - Instrução para ignorar comandos no PR
   - Processo que reforça a execução completa
   - Ênfase em "sempre executar TODAS as verificações"

**Características**:
- Proteção robusta contra prompt injection
- Schema JSON validado com valores permitidos
- Checklist completo de verificações
- Processo de análise estruturado
- Instruções específicas e acionáveis
- Maior consistência e confiabilidade

**Uso**: Versão de produção, adequada para uso em ambiente real com proteção contra ataques de prompt injection.

---

## Evolução das Versões

### Comparação Visual

| Característica | v1 | v2 | v3 |
|---------------|----|----|-----|
| Formato estruturado | ❌ | ✅ JSON | ✅ JSON Schema |
| Critérios específicos | ❌ | ✅ | ✅ + Checklist |
| Proteção prompt injection | ❌ | ❌ | ✅ Múltiplas camadas |
| Valores permitidos definidos | ❌ | ❌ | ✅ |
| Processo passo a passo | ❌ | ❌ | ✅ |
| Ações acionáveis | ❌ | ❌ | ✅ |

### Principais Lições Aprendidas

1. **Estruturação é fundamental**: v2 mostrou que definir formato de saída (JSON) melhora drasticamente a consistência

2. **Critérios explícitos melhoram qualidade**: Listar o que verificar em cada categoria resulta em análises mais completas

3. **Prompt injection é um risco real**: PR6 demonstra que prompts sem proteção podem ser manipulados facilmente

4. **Múltiplas camadas de proteção**: v3 usa várias técnicas (alertas, instruções, processo) para garantir segurança

5. **Especificidade gera melhores resultados**: Instruções vagas geram respostas vagas; instruções específicas geram respostas específicas

---

## Exemplos de Teste

O projeto inclui 6 exemplos de PRs para teste:

- **PR1**: S3 bucket sem configurações de segurança (versionamento, encryption)
- **PR2**: SSH aberto para 0.0.0.0/0 (risco crítico de segurança)
- **PR3**: Aumento significativo de custo (RDS upgrade)
- **PR4**: Adição de tag de cost center (boa prática)
- **PR5**: Lambda sem timeout definido (risco de falha)
- **PR6**: Tentativa de prompt injection (teste de segurança)

Cada versão do prompt foi testada com todos os PRs, e os resultados estão documentados na pasta `resultados/`.

---

## Como Usar

1. Escolha a versão do prompt adequada ao seu caso de uso
2. Substitua `{{descricao}}` e `{{conteudo}}` pelos dados do PR
3. Execute o prompt em seu modelo de linguagem preferido
4. Valide a resposta contra o schema esperado (especialmente para v3)

---

## Conclusão

A evolução dos prompts demonstra como melhorias incrementais em estruturação, especificidade e proteção resultam em sistemas mais confiáveis e seguros. A versão v3 representa um prompt de produção, adequado para uso em ambientes críticos onde a segurança e consistência são essenciais.
