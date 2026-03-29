---
name: etl
description: >
  ETL de dados MRP do Sankhya para o template de Campanhas de Marketing da Rampap.
  Transforma o export bruto do MRP em dados estruturados dentro do template de campanha,
  filtrando produtos inativos e em ruptura. Use esta skill sempre que o usuário mencionar
  ETL de campanhas, importar dados MRP, preparar template de campanha, carregar dados
  de produtos para campanhas, ou qualquer variação de "rodar o ETL da campanha".
  Também use quando o usuário fornecer um arquivo Excel do MRP e quiser popular o
  template de campanhas PRs.
---

# ETL — Campanhas de Marketing Rampap

Skill para executar o processo de ETL (Extract, Transform, Load) dos dados MRP exportados
do Sankhya para o template de Campanhas PRs da Rampap.

## Quando NÃO usar

- Para análise dos dados já carregados no template — use skills de análise (futuras)
- Para gerar gráficos ou apresentações — use skills de relatório (futuras)
- Para editar manualmente dados de campanha (PRx, IT PRx, Inc PRx)

## Visão geral do processo

O ETL recebe dois arquivos:
1. **Export MRP** — arquivo Excel gerado pela tela MRP do Sankhya (sheet única, ~6.000 linhas, 89 colunas A-CK)
2. **Template de Campanha** — arquivo Excel com 18 abas (MRP ativos, PRx, IT PRx, Inc PRx)

O resultado é o template de campanha populado com os dados filtrados do MRP.

## Pré-requisitos

- Python 3.8+ com `openpyxl` instalado (`pip install openpyxl`)
- Os dois arquivos Excel na mesma pasta ou em caminhos acessíveis

## Passo a passo

### Step 1: Identificar os arquivos

Pergunte ao usuário (se ainda não informou):
- Caminho do **export MRP do Sankhya** (arquivo com sheet única "new sheet")
- Caminho do **template de campanha** (arquivo com abas "MRP ativos", "IT PR1", etc.)

Se o usuário passar apenas um arquivo, identifique qual é pelo conteúdo:
- Export MRP: sheet única chamada "new sheet", linha 1 contém "arquivo", linha 2 contém "Emissão:"
- Template: múltiplas abas incluindo "MRP ativos", "IT PR1", "Template", "Racional"

### Step 2: Executar o script ETL

Execute o script bundled `scripts/etl_mrp.py` passando os caminhos dos arquivos:

```bash
python <skill-path>/scripts/etl_mrp.py --mrp "<caminho-export-mrp>" --template "<caminho-template>" --output "<caminho-saida>"
```

O script realiza todas as transformações automaticamente. Se o usuário não especificar
o caminho de saída, gere o arquivo na mesma pasta do template com sufixo `_ETL`.

### Step 3: Validar resultado

Após a execução, reporte ao usuário:
1. Quantas linhas o export MRP tinha originalmente
2. Quantas linhas ficaram em **MRP ativos** (após filtro Ativo = "N")
3. Quantas linhas ficaram em **IT PR1** (após filtro Em ruptura = 1)
4. Se as colunas calculadas (CL-CT) do IT PR1 foram preservadas

### Step 4: Disponibilizar para análise

Informe ao usuário que o template está pronto e sugira próximos passos:
- Revisar os dados no Excel
- Usar skills de análise de campanha (quando disponíveis)
- Gerar relatórios ou apresentações

## Detalhes técnicos do ETL

Para referência, o script `etl_mrp.py` executa estes passos:

### Extract (Extração)
1. Abrir o export MRP do Sankhya
2. Ignorar as 2 primeiras linhas (metadados: "arquivo", "Emissão:...") e a última linha
3. Linha 3 contém os cabeçalhos reais (89 colunas, A até CK)
4. Linhas 4 em diante são os dados

### Transform (Transformação)
5. Filtrar: manter apenas linhas onde coluna **BP ("Ativo") = "N"** (produtos inativos)
6. Do resultado acima, criar segundo filtro: manter apenas linhas onde coluna **CF ("Em ruptura") = 1**

### Load (Carga)
7. Abrir o template de campanha
8. Na aba **"MRP ativos"**: limpar dados existentes (A2 até CK), preservar cabeçalho (linha 1), colar dados filtrados por Ativo = "N"
9. Na aba **"IT PR1"**: limpar dados existentes (A2 até CK), preservar cabeçalho (linha 1), colar dados filtrados por Em ruptura = 1
10. Preservar todas as outras abas intactas (Template, Racional, PRx, IT PR2-5, Inc PRx)
11. Preservar fórmulas nas colunas calculadas de IT PR1 (CL até CT) — o script cola apenas nas colunas A-CK

## Schema dos dados

Consulte `references/data_schema.md` para o dicionário completo das 89 colunas,
tipos de dados e valores esperados.

## Estrutura do template de campanha

| Aba | Conteúdo | Modificada pelo ETL? |
|-----|----------|---------------------|
| Template | Texto introdutório | Não |
| Racional | Metodologia das campanhas | Não |
| **MRP ativos** | Catálogo de produtos (Ativo="N") | **Sim** |
| PR1-PR5 | Descrição de cada campanha | Não |
| **IT PR1** | Itens da campanha 1 (Ruptura=1) | **Sim** |
| IT PR2-PR5 | Itens das campanhas 2-5 | Não |
| Inc PR1-PR5 | Resumos de incremento | Não (recalcula via fórmulas) |
