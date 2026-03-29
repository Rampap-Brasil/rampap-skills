# Schema dos Dados MRP — Dicionário de Colunas

89 colunas (A até CK) do export MRP do Sankhya.

## Identificação do Produto (A-N)

| Col | Nome | Tipo | Descrição |
|-----|------|------|-----------|
| A | Grupo | texto | Grupo do produto |
| B | Subgrupo | texto | Subgrupo |
| C | Marca | texto | Marca do fabricante |
| D | Master | texto | Código master |
| E | Categoria | texto | Categoria do produto |
| F | Fabricante | texto | Nome do fabricante |
| G | UF Fab | texto | Estado do fabricante |
| H | Cidade Fab | texto | Cidade do fabricante |
| I | Cod. Bemol | inteiro | Código interno Bemol |
| J | Cod. Barras | texto | Código de barras (EAN) |
| K | Cod. Fab | texto | Código do fabricante |
| L | Cod. Rampap | inteiro | Código interno Rampap |
| M | Produto | texto | Nome/descrição do produto |
| N | UN | texto | Unidade de medida |

## Vendas Mensais (O-AP) — Padrão repetido por 7 meses

Cada mês tem 4 colunas: Qtd, Vlr, Prom, % Desc.

| Período | Qtd | Vlr (R$) | Prom (R$) | % Desc |
|---------|-----|----------|-----------|--------|
| mes-6 | O | P | Q | R |
| mes-5 | S | T | U | V |
| mes-4 | W | X | Y | Z |
| mes-3 | AA | AB | AC | AD |
| mes-2 | AE | AF | AG | AH |
| mes-1 | AI | AJ | AK | AL |
| mes atual | AM | AN | AO | AP |

- **Qtd**: quantidade vendida (inteiro)
- **Vlr**: valor de venda (decimal, R$)
- **Prom**: valor em promoção (decimal, R$)
- **% Desc**: percentual de desconto aplicado (decimal, %)

## Giro e Classificação ABC (AQ-AX)

| Col | Nome | Tipo | Descrição |
|-----|------|------|-----------|
| AQ | Giro90d | decimal | Giro dos últimos 90 dias |
| AR | Giro60d | decimal | Giro dos últimos 60 dias |
| AS | Giro30d | decimal | Giro dos últimos 30 dias |
| AT | Giro15d | decimal | Giro dos últimos 15 dias |
| AU | Giro mes atual | decimal | Giro do mês atual |
| AV | ABC Qtd | texto | Classificação ABC por quantidade (A/B/C) |
| AW | ABC Vlr | texto | Classificação ABC por valor |
| AX | ABC Mrg | texto | Classificação ABC por margem |

## Estoque (AY-BF)

| Col | Nome | Tipo | Descrição |
|-----|------|------|-----------|
| AY | Est atual | inteiro | Estoque atual |
| AZ | Est bloqueado | inteiro | Estoque bloqueado |
| BA | Est transito | inteiro | Estoque em trânsito |
| BB | Est total | inteiro | Estoque total |
| BC | Est res | inteiro | Estoque reservado |
| BD | Est disp | inteiro | Estoque disponível |
| BE | Cob atual | decimal | Cobertura atual (dias) |
| BF | Custo unit | decimal | Custo unitário (R$) |

## Custos e Preços (BG-BU)

| Col | Nome | Tipo | Descrição |
|-----|------|------|-----------|
| BG | Custo rep | decimal | Custo de reposição (R$) |
| BH | Novo(90d) | texto | Se é produto novo nos últimos 90 dias (S/N) |
| BI | Preco tabela | decimal | Preço de tabela (R$) |
| BJ | Mark-up | decimal | Mark-up (%) |
| BK | Preco Bemol | decimal | Preço Bemol (R$) |
| BL | Dt cadastro | data | Data de cadastro |
| BM | Dt ult comp | data | Data da última compra |
| BN | Dt ult ent | data | Data da última entrada |
| BO | Dt ult venda | data | Data da última venda |
| BP | **Ativo** | texto | Produto ativo: "S" (sim) / "N" (não) |
| BQ | Custo est atual | decimal | Custo estoque atual (R$) |
| BR | Custo est transito | decimal | Custo estoque em trânsito (R$) |
| BS | Custo est total | decimal | Custo estoque total (R$) |
| BT | Preco est atual | decimal | Preço estoque atual (R$) |
| BU | Preco est total | decimal | Preço estoque total (R$) |

## Status e Flags (BV-CE)

| Col | Nome | Tipo | Descrição |
|-----|------|------|-----------|
| BV | Ativo compras | texto | Ativo para compras: "S"/"N" |
| BW | CST | inteiro | Código de Situação Tributária |
| BX | Em showroom | texto | Exposto em showroom: "S"/"N" |

### Flags por loja (presença marcada com "X"):

| Col | Loja |
|-----|------|
| BY | Cidade Nova |
| BZ | Torquato |
| CA | Matriz |
| CB | Manauara |
| CC | Nova Cidade |
| CD | Camapua |
| CE | AM Shopping |

## Ruptura e Sugestões (CF-CK)

| Col | Nome | Tipo | Descrição |
|-----|------|------|-----------|
| CF | **Em ruptura** | inteiro | Em ruptura: 1 (sim) / vazio (não) |
| CG | Sug Systock | inteiro | Sugestão Systock (quantidade) |
| CH | Dt pri ent | data | Data da primeira entrada |
| CI | Cob total | decimal | Cobertura total (dias) |
| CJ | Est pend | inteiro | Estoque pendente |
| CK | Cob futura | decimal | Cobertura futura (dias) |

## Colunas Calculadas no IT PR1 (CL-CT)

Estas colunas existem apenas na aba IT PR1 do template e contêm fórmulas:

| Col | Nome | Fórmula | Descrição |
|-----|------|---------|-----------|
| CL | Venda dos últimos 90 dias | =AJ+AF+AB | Soma Vlr dos meses -1, -2, -3 |
| CM | Média dos últimos 90 dias | =CL/3 | Média mensal de faturamento |
| CN | Increm (%) esperado | (manual) | Percentual de incremento definido pelo gestor |
| CO | Meta de Faturamento | =CM+(CM*CN) | Meta mensal com incremento |
| CP | Increm (R$) esperado | =CM*CN | Incremento em reais |
| CQ | Qtd dos últimos 90 dias | =AI+AE+AA | Soma Qtd dos meses -1, -2, -3 |
| CR | QTD Média dos últimos 90 dias | =CQ/3 | Média mensal de quantidade |
| CS | Campanha | (manual) | Nome/código da campanha |
| CT | Promoção | (manual) | Tipo de promoção aplicada |
